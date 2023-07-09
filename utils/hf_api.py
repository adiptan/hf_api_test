import requests
from urllib.parse import urljoin


def get_hf_data(
        base_url: str,
        end_point: str,
        hf_token: str,
        page: int = 1,
):
    headers = {
        "Authorization": f"Bearer {hf_token}",
    }
    params = {
        "page": page
    }

    url = urljoin(base_url, end_point)
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()
