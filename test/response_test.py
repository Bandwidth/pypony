import requests

from api_validator.models import Response


def test_delegation():
    req_response = requests.get("http://localhost:8000")
    response = Response(req_response)

    assert response.body == req_response.json()
    assert response.content == req_response.content
    assert response.encoding == req_response.encoding
    assert response.headers == req_response.headers
    assert response.status_code == req_response.status_code


def test_body_type_list():
    response = Response(requests.get("http://jservice.io/api/clues?category=4642&value=500"))

    assert isinstance(response.body, list)
