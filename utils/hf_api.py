import requests
from urllib.parse import urljoin


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
        base_url,
        end_point: str,
        headers: dict,
        body: dict,
):
    url = urljoin(base_url, end_point)
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()

    return response.json()