import pytest
from hamcrest import assert_that, is_, has_items, instance_of
from requests.structures import CaseInsensitiveDict

from src.models import Request


class TestRequestModel:
    """Class for basic unit testing of the Request model"""

    headers = {"Content-Type": "application/json"}

    request = Request(
        base_url="https://api.test.com",
        method="GET",
        path="/api/v1/test",
        params={},
        headers=headers,
        global_auth={},
        auth={},
        body={},
    )

    def test_request_model(self):
        assert_that(self.request.base_url, is_("https://api.test.com"))
        assert_that(self.request.method, is_("GET"))
        assert_that(self.request.path, is_("/api/v1/test"))
        assert_that(self.request.params, is_({}))
        assert_that(self.request.headers, is_(self.headers))
        assert_that(self.request.global_auth, is_({}))
        assert_that(self.request.auth, is_({'username': '', 'password': ''}))
        assert_that(self.request.body, is_({}))
