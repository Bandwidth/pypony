import pytest
import requests
from jsonschema import ValidationError

from src.parsing import parse_steps_file, parse_spec_file
from src.requests import make_requests


class TestRequests:
    """Class for basic unit testing of the requests.py module"""

    steps_file_path = "./tests/fixtures/valid/steps/person_api.yml"
    spec_file_path = "./tests/fixtures/valid/specs/person_api.yml"

    valid_test_steps = parse_steps_file(steps_file_path)
    valid_test_spec, operationSchemas = parse_spec_file(valid_test_steps, spec_file_path)

    def test_make_requests_with_valid_steps_and_spec(self, mocker):
        mock_response1 = requests.Response()
        mock_response1.status_code = 201
        mock_response1.headers = {}
        mock_response1.body = '{"id": 1}'
        mock_response1._content = b'{"id": 1}'
        mock_response1._text = mock_response1.content.decode('utf-8')

        mock_response2 = requests.Response()
        mock_response2.status_code = 200
        mock_response2.headers = {}
        mock_response2.body = '{"age": 29, "name": {"first": "test", "last": "test"}}'
        mock_response2._content = b'{"age": 29, "name": {"first": "test", "last": "test"}}'
        mock_response2._text = mock_response1.content.decode('utf-8')

        mock_responses = [mock_response1, mock_response2]
        mock_request = mocker.Mock(side_effect=mock_responses)
        mocker.patch('requests.request', new=mock_request)

        make_requests(self.valid_test_steps, self.operationSchemas, False, False)

    def test_make_requests_with_invalid_response(self, mocker):
        mock_response1 = requests.Response()
        mock_response1.status_code = 201
        mock_response1.headers = {}
        mock_response1.body = '{"id": 1}'
        mock_response1._content = b'{"id": 1}'
        mock_response1._text = mock_response1.content.decode('utf-8')

        mock_response2 = requests.Response()
        mock_response2.status_code = 200
        mock_response2.headers = {}
        # required property age is missing
        mock_response2.body = '{"name": {"first": "test", "last": "test"}}'
        mock_response2._content = b'{"name": {"first": "test", "last": "test"}}'
        mock_response2._text = mock_response1.content.decode('utf-8')

        mock_responses = [mock_response1, mock_response2]
        mock_request = mocker.Mock(side_effect=mock_responses)
        mocker.patch('requests.request', new=mock_request)

        with pytest.raises(ValidationError):
            make_requests(self.valid_test_steps, self.operationSchemas, False, False)
