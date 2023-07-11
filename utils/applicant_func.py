import unicodedata
from pathlib import Path
from utils.hf_api import post_request


def get_candidate_file_path(position_path: Path, candidate_name: str):
    candidate_name = unicodedata.normalize("NFKC", candidate_name).strip().lower()

    for file in position_path.iterdir():
        file_name = unicodedata.normalize("NFKC", Path(file).stem).strip().lower()

        if candidate_name != file_name:
            continue

        return file

    return


def prepare_candidate_body(
    full_name: str,
    money: str,
) -> dict:
    first_name = full_name.split()[0]
    last_name = full_name.split()[1]

    body = {
        "first_name": first_name,
        "last_name": last_name,
        "money": money,
    }

    if len(full_name.split()) > 2:
        middle_name = full_name.split()[2]
        body["middle_name"] = middle_name

    return body


def create_candidate(
    base_url: str,
    org_id: str,
    headers: dict,
    body: dict,
):
    return post_request(base_url, f"accounts/{org_id}/applicants", headers, body)
