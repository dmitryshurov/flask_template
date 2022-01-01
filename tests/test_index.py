import requests


def test_index():
    response = requests.get('http://127.0.0.1:8080')
    response.raise_for_status()
    assert response.json() == {"message": "Hello"}
