from src.models.request import Request
from src.preprocessing import evaluate

from rich import inspect


class Step:
    def __init__(
        self,
        step: dict,
        steps: dict,
    ):
        for key in step:
            step[key] = evaluate(step[key], steps)

        self.name = step["name"]
        self.operation_id = step["operation_id"]
        self.method = step["method"]
        self.path = step["path"]
        self.status_code = step["status_code"]

        if "headers" in step:
            self.headers = step["headers"]
        else:
            self.headers = None

        if "body" in step:
            self.body = step["body"]
        else:
            self.body = None

        if "raw_body" in step:
            self.body = step["raw_body"]

        if "params" in step:
            self.params = step["params"]
        else:
            self.params = None

        if "auth" in step:
            self.auth = step["auth"]
        else:
            self.auth = None

    def construct_request(self, base_url, global_auth):
        return Request(
            base_url=base_url,
            method=self.method,
            path=self.path,
            params=self.params,
            headers=self.headers,
            global_auth=global_auth,
            auth=self.auth,
            body=self.body,
        )
