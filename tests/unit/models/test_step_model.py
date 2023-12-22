import pytest

from src.models import Step


class TestStepModel:
    step = Step(
        step={
            "name": "test",
            "operation_id": "test",
            "method": "GET",
            "path": "/api/v1/test",
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {},
            "params": {},
            "auth": {},
        },
        steps={},
    )

    rawBodyStep = Step(
        step={
            "name": "test",
            "operation_id": "test",
            "method": "GET",
            "path": "/api/v1/test",
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "raw_body": "123",
            "params": {},
            "auth": {},
        },
        steps={},
    )

    barebonesStep = Step(
        step={
            "name": "test",
            "operation_id": "test",
            "method": "GET",
            "path": "/api/v1/test",
            "status_code": 200,
        },
        steps={},
    )

    def test_step_model(self):
        assert self.step.name == "test"
        assert self.step.operation_id == "test"
        assert self.step.method == "GET"
        assert self.step.path == "/api/v1/test"
        assert self.step.status_code == 200
        assert self.step.headers == {"Content-Type": "application/json"}
        assert self.step.body == {}
        assert self.step.params == {}
        assert self.step.auth == {}

    def test_barebones_step_model(self):
        assert self.barebonesStep.name == "test"
        assert self.barebonesStep.operation_id == "test"
        assert self.barebonesStep.method == "GET"
        assert self.barebonesStep.path == "/api/v1/test"
        assert self.barebonesStep.status_code == 200
        assert self.barebonesStep.headers is None
        assert self.barebonesStep.body is None
        assert self.barebonesStep.params is None
        assert self.barebonesStep.auth is None

    def test_construct_request(self):
        request = self.step.construct_request(
            base_url="https://api.test.com",
            global_auth={},
        )
        assert request.base_url == "https://api.test.com"
        assert request.method == "GET"
        assert request.path == "/api/v1/test"
        assert request.params == {}
        assert request.headers == {"Content-Type": "application/json"}
        assert request.global_auth == {}
        assert request.auth == {'username': '', 'password': ''}
        assert request.body == {}

    def test_construct_request_raw_body(self):
        request = self.rawBodyStep.construct_request(
            base_url="https://api.test.com",
            global_auth={},
        )
        assert request.base_url == "https://api.test.com"
        assert request.method == "GET"
        assert request.path == "/api/v1/test"
        assert request.params == {}
        assert request.headers == {"Content-Type": "application/json"}
        assert request.global_auth == {}
        assert request.auth == {'username': '', 'password': ''}
        assert request.body == "123"
