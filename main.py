import os

from collections import namedtuple
from pathlib import Path

import requests
from dotenv import load_dotenv
from loguru import logger

from utils.common_func import (
    get_cells,
    get_args,
    get_xlsx_file_path,
    read_progress_file,
)
from utils.hf_api import post_request, upload_file, get_hf_data
from utils.applicant_func import (
    prepare_candidate_body,
    get_candidate_file_path,
)
from utils.vacancy_func import (
    get_vacancies,
    get_vacancy_status_id,
    prepare_vacancy_body,
)


def main():
    db_path = get_args()

    try:
        if not Path(db_path).exists():
            raise FileNotFoundError
    except FileNotFoundError:
        logger.error(f"Directory '{db_path}' not found.")
        return

    try:
        xlsx_file = get_xlsx_file_path(db_path)
    except FileNotFoundError:
        logger.error(f"There is no xlsx-file found in directory '{db_path}'. Exit.")
        return

    progress_file = Path("progress.txt")

    start_message = "------Start candidates import------"
    row_number = 2

    if progress_file.exists():
        row_number += read_progress_file(progress_file)
        start_message = f"------Start import row {row_number} ------"

    candidates = get_cells(xlsx_file, 5, row_number)

    column_name = [
        "position",
        "full_name",
        "salary",
        "comment",
        "status",
    ]
    Row = namedtuple(
        "Row",
        column_name,
    )

    load_dotenv()

    base_url: str = os.environ["URL"]
    hf_token: str = os.environ["TOKEN"]

    headers = {
        "Authorization": f"Bearer {hf_token}",
    }
    params = {}

    try:
        org_id = get_hf_data(base_url, "accounts", headers, params).get("items")[0].get("id")
    except requests.exceptions.RequestException as error:
        logger.error(f"Error found while get account id: {error}")
        return

    try:
        vacancies = get_vacancies(base_url, org_id, headers)
    except requests.exceptions.RequestException as error:
        logger.error(f"Error found while get vacancies: {error}")
        return

    try:
        end_point = f"accounts/{org_id}/vacancies/statuses"
        statuses = get_hf_data(base_url, end_point, headers, params).get("items")
    except requests.exceptions.RequestException as error:
        logger.error(f"Error found while get status_id: {error}")
        return

    logger.info(start_message)

    for row_id, candidate in enumerate(candidates, 1):
        current_row = Row(*candidate)

        logger.info(
            "Processing string: {}, candidate: {}".format(
                row_id,
                current_row.full_name.strip(),
            )
        )

        progress_file.write_text(str(row_id))

        file_path = Path.joinpath(db_path, current_row.position)
        candidate_file = get_candidate_file_path(file_path, current_row.full_name)
        status_id = get_vacancy_status_id(statuses, current_row.status)

        try:
            uploaded_file_id: int = upload_file(
                base_url, f"accounts/{org_id}/upload", headers, candidate_file
            ).get("id")
        except requests.exceptions.RequestException as error:
            logger.error(f"Error found while upload candidate file: {error}")
            return

        candidate_body = prepare_candidate_body(
            current_row.full_name, current_row.salary, uploaded_file_id
        )

        try:
            candidate_id: int = post_request(
                base_url, f"accounts/{org_id}/applicants", headers, candidate_body
            ).get("id")
        except requests.exceptions.RequestException as error:
            logger.error(f"Error found while create candidate: {error}")
            return

        vacancy_body = prepare_vacancy_body(
            vacancies, current_row.position, status_id, current_row.comment
        )

        try:
            post_request(
                base_url,
                f"accounts/{org_id}/applicants/{candidate_id}/vacancy",
                headers,
                vacancy_body,
            )
        except requests.exceptions.RequestException as error:
            logger.error(f"Error found while add candidate on vacancy: {error}")
            return

        logger.info("Candidate processed.")

    logger.info("------Candidates import ended------")

    progress_file.unlink()


if __name__ == "__main__":
    main()
