import requests
from urllib.parse import urljoin
from pathlib import Path
from mimetypes import guess_type


def get_hf_data(
    base_url: str,
    end_point: str,
    headers: dict,
    params: dict,
) -> dict:
    url = urljoin(base_url, end_point)
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def post_request(
    base_url: str,
    end_point: str,
    headers: dict,
    body: dict,
) -> dict:
    url = urljoin(base_url, end_point)
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    return response.json()


def upload_file(
    base_url: str,
    end_point: str,
    headers: dict,
    file_path: Path,
) -> dict:
    url = urljoin(base_url, end_point)
    filename = file_path.name
    mimetype = guess_type(filename)[0]

    with open(file_path, "rb") as file:
        files = {"file": (filename, file, mimetype)}
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()

        return response.json()
