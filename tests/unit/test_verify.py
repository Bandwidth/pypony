import pytest
from hamcrest import assert_that, is_, has_items, instance_of

from src.verify import *
from src.models import Response


class TestVerify:
    """Class for basic unit testing of the verify.py module"""

    schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
    }

    def test_verify_request_body_with_valid_request_body(self):
        request_body = {"name": "John Doe", "age": 30}
        assert_that(verify_request_body(request_body, self.schema), is_(None))

    def test_verify_request_body_with_invalid_request_body(self):
        request_body = {"name": "John Doe", "age": "30"}
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }
        with pytest.raises(ValidationError):
            verify_request_body(request_body, self.schema)

    def test_verify_response_with_valid_response(self):
        status_code = 200
        data = {"name": "John Doe", "age": 30}
        response = Response(status_code, {}, data)
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }

        assert_that(verify_response(response, status_code, self.schema), is_(None))

    def test_verify_response_with_invalid_response(self):
        status_code = 200
        data = {"name": "John Doe", "age": "30"}
        response = Response(status_code, {}, data)
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        }

        with pytest.raises(ValidationError):
            verify_response(response, status_code, self.schema)
