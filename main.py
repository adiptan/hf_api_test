import os
import unicodedata

from collections import namedtuple
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
from loguru import logger

from utils.common_func import get_cells, get_args
from utils.hf_api import get_hf_data


def get_candidate_file_path(position_path: Path, candidate_name: str):
    candidate_name = unicodedata.normalize('NFKC', candidate_name).strip().lower()
    for file in position_path.iterdir():
        file_name = unicodedata.normalize('NFKC', Path(file).stem).strip().lower()

        if candidate_name == file_name:
            continue

        return file

    return


def get_xlsx_file_path(directory: Path):
    for file in directory.iterdir():
        if file.suffix == ".xlsx":
            return file
    raise FileNotFoundError


def get_vacancy_id_by_name(vacancies: list, vacancy_name: str):
    vacancy_id = ''

    for vacancy in vacancies:
        pprint(vacancy)


def get_vacancies(
        base_url: str,
        org_id: str,
        hf_token: str,
) -> list:

    page_data = get_hf_data(base_url, f"accounts/{org_id}/vacancies", hf_token)
    total_pages = page_data["total_pages"]
    vacancies: list = page_data["items"]

    if page_data["total_pages"] > 1:
        for page in range(1, total_pages):
            page_data = get_hf_data(base_url, f"accounts/{org_id}/vacancies", hf_token, page+1)
            vacancies.extend(page_data["items"])

    return vacancies


def main():
    hf_token, db_path = get_args()

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
        "state",
    ]
    Row = namedtuple(
        "Row",
        column_name,
    )
    # TOKEN = a841c687571a510970a1cbf1dac44c987cbd0c287b487eb54e4d8daed5f29537
    load_dotenv()
    org_id = os.environ["ORG_ID"]
    base_url = os.environ["URL"]

    vacancies = get_vacancies(base_url, org_id, hf_token)

    pprint(len(vacancies))

    # get_vacancy_id(all_vacancies, "Frontend-разработчик")

    # for candidate_id, candidate in enumerate(candidates, 1):
    #     current_row = Row(*candidate)
    #     file_path = Path.joinpath(argv.db_path, current_row.position)
    #     candidate_file = get_candidate_file_path(file_path, current_row.full_name)
    #     logger.info("Processing candidate: {}. "
    #                 "File path: {}".format(current_row.full_name.strip(),
    #                                        candidate_file))


if __name__ == '__main__':
    main()
