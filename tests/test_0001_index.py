import requests

from .helpers import BASE_URL


def test_0001_index():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    assert response.json() == {"message": "Hello"}
