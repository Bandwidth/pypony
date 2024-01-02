from hamcrest import assert_that, is_
import requests

from src.models import Request

pytest_plugins = ("pytest_mock",)


class TestRequestModel:
    """Class for basic unit testing of the Request model"""

    headers = {"Content-Type": "application/json"}

    jsonRequest = Request(
        base_url="https://api.test.com",
        method="GET",
        path="/api/v1/test",
        params={},
        headers=headers,
        global_auth={},
        auth={},
        body={},
    )

    rawBodyRequest = Request(
        base_url="https://api.test.com",
        method="GET",
        path="/api/v1/test",
        params={},
        headers=headers,
        global_auth={"username": "test", "password": "test"},
        auth={},
        body="123",
    )

    def test_json_request_model(self):
        assert_that(self.jsonRequest.base_url, is_("https://api.test.com"))
        assert_that(self.jsonRequest.method, is_("GET"))
        assert_that(self.jsonRequest.path, is_("/api/v1/test"))
        assert_that(self.jsonRequest.params, is_({}))
        assert_that(self.jsonRequest.headers, is_(self.headers))
        assert_that(self.jsonRequest.global_auth, is_({}))
        assert_that(self.jsonRequest.auth, is_({'username': '', 'password': ''}))
        assert_that(self.jsonRequest.body, is_({}))

    def test_raw_body_request_model(self):
        assert_that(self.rawBodyRequest.base_url, is_("https://api.test.com"))
        assert_that(self.rawBodyRequest.method, is_("GET"))
        assert_that(self.rawBodyRequest.path, is_("/api/v1/test"))
        assert_that(self.rawBodyRequest.params, is_({}))
        assert_that(self.rawBodyRequest.headers, is_(self.headers))
        assert_that(self.rawBodyRequest.global_auth, is_({'username': 'test', 'password': 'test'}))
        assert_that(self.rawBodyRequest.auth, is_({'username': 'test', 'password': 'test'}))
        assert isinstance(self.rawBodyRequest.body, str)
        assert_that(self.rawBodyRequest.body, is_("123"))

    def test_send_json_request(self, mocker):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.data = {}
        mocker.patch.object(requests, 'request', return_value=mock_response)

        response = self.jsonRequest.send()
        assert_that(response.status_code, is_(200))
        assert_that(response.headers, is_({}))
        assert_that(response.body, is_(''))

    def test_send_raw_body_request(self, mocker):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.data = {}
        mocker.patch.object(requests, 'request', return_value=mock_response)

        response = self.rawBodyRequest.send()
        assert_that(response.status_code, is_(200))
        assert_that(response.headers, is_({}))
        assert_that(response.body, is_(''))
