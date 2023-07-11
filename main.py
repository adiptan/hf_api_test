import os

from collections import namedtuple
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from utils.common_func import get_cells, get_args, get_xlsx_file_path
from utils.hf_api import post_request, upload_file
from utils.applicant_func import (
    create_candidate,
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

    candidates = get_cells(xlsx_file, 5, 2)

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

    org_id = os.environ["ORG_ID"]
    base_url = os.environ["URL"]
    hf_token = os.environ["TOKEN"]

    headers = {
        "Authorization": f"Bearer {hf_token}",
    }

    vacancies = get_vacancies(base_url, org_id, headers)

    for str_id, candidate in enumerate(candidates, 1):
        current_row = Row(*candidate)
        file_path = Path.joinpath(db_path, current_row.position)
        candidate_file = get_candidate_file_path(file_path, current_row.full_name)

        uploaded_file_id: int = upload_file(
            base_url, f"accounts/{org_id}/upload", headers, candidate_file
        ).get("id")

        candidate_body = prepare_candidate_body(
            current_row.full_name, current_row.salary, uploaded_file_id
        )

        candidate_id = create_candidate(base_url, org_id, headers, candidate_body)["id"]
        status_id = get_vacancy_status_id(base_url, org_id, headers, current_row.status)
        logger.info(
            "Processing string: {}, candidate: {}".format(
                str_id,
                current_row.full_name.strip(),
            )
        )

        vacancy_body = prepare_vacancy_body(
            vacancies, current_row.position, status_id, current_row.comment
        )

        if not vacancy_body:
            logger.warning("Error while add candidate on vacancy.")

        post_request(
            base_url,
            f"accounts/{org_id}/applicants/{candidate_id}/vacancy",
            headers,
            vacancy_body,
        )

        logger.info("Candidate processed.")


if __name__ == "__main__":
    main()
