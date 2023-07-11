from typing import Optional, Union

from utils.hf_api import get_hf_data


def prepare_vacancy_body(
    vacancies: list,
    position: str,
    status_id: int,
    comment: str,
) -> Optional[dict[str, Union[list[dict], str, int]]]:
    vacancy_id: int = get_vacancy_id_by_name(vacancies, position)

    if not vacancy_id:
        return

    vacancy_body = {
        "vacancy": vacancy_id,
        "status": status_id,
        "comment": comment,
    }

    return vacancy_body


def get_vacancy_id_by_name(vacancies: list, vacancy_name: str) -> Optional[int]:
    for vacancy in vacancies:
        position: str = vacancy.get("position")
        vacancy_id: int = vacancy.get("id")

        if position.strip().lower() != vacancy_name.strip().lower():
            continue

        return vacancy_id

    return


def get_vacancies(
    base_url: str,
    org_id: str,
    headers: dict,
) -> list:
    params = {
        "page": 1,
    }

    page_data = get_hf_data(base_url, f"accounts/{org_id}/vacancies", headers, params)
    total_pages = page_data["total_pages"]
    vacancies: list = page_data["items"]

    if page_data["total_pages"] > 1:
        for page in range(1, total_pages):
            params["page"] += 1
            page_data = get_hf_data(
                base_url, f"accounts/{org_id}/vacancies", headers, params
            )
            vacancies.extend(page_data["items"])

    return vacancies


def get_vacancy_status_id(
    base_url: str,
    org_id: str,
    headers: dict,
    search_status: str,
) -> Optional[int]:
    params = {}
    end_point = f"accounts/{org_id}/vacancies/statuses"
    statuses = get_hf_data(base_url, end_point, headers, params)["items"]

    for status in statuses:
        status_name: str = status.get("name").strip()
        status_id: int = status.get("id")

        if status_name != search_status.strip():
            continue

        return status_id

    return
