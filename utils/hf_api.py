import requests
from urllib.parse import urljoin
from pathlib import Path
from mimetypes import guess_type
from loguru import logger


def get_hf_data(
        base_url: str,
        end_point: str,
        headers: dict,
        params: dict,
) -> dict:
    url = urljoin(base_url, end_point)
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as error:
        logger.error(f"Error found while get request: {error}")


def post_request(
        base_url: str,
        end_point: str,
        headers: dict,
        body: dict,
):
    url = urljoin(base_url, end_point)
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as error:
        logger.error(f"Error found while post request: {error}")


def upload_file(
        base_url: str,
        end_point: str,
        headers: dict,
        file_path: Path,
):
    url = urljoin(base_url, end_point)
    filename = file_path.name
    mimetype = guess_type(filename)[0]

    with open(file_path, "rb") as file:
        files = {"file": (filename, file, mimetype)}
        try:
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logger.error(f"Error found while upload file: {error}")
            raise error

        return response.json()
