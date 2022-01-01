import os

import requests


def test_index():
    response = requests.get(f'http://nginx:{os.environ["BACKEND_INTERNAL_PORT"]}')

    response.raise_for_status()
    assert response.json() == {"message": "Hello"}
