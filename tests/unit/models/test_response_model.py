import pytest
from hamcrest import assert_that, is_, has_items, instance_of
from requests.structures import CaseInsensitiveDict

from src.models import Response


class TestResponseModel:
    """Class for basic unit testing of the Response model"""
    headers = {"Content-Type": "application/json"}
    data = {"test": "test"}

    response = Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        data={"test": "test"},
    )

    def test_response_model(self):
        assert_that(self.response.status_code, is_(200))
        assert_that(self.response.headers, is_(self.headers))
        assert_that(self.response.data, is_(self.data))
