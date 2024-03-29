import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict
from typing import Union

from src.models.response import Response


class Request:
    def __init__(
        self,
        base_url: str,
        method: str,
        path: str,
        params: dict,
        headers: dict,
        global_auth: dict,
        auth: dict,
        body: Union[dict, str],
    ):
        self.base_url = base_url
        self.method = method
        self.path = path
        self.params = params
        self.headers = headers
        self.global_auth = global_auth
        self.auth = auth
        self.body = body

        if not self.auth:
            if not self.global_auth:
                self.auth = {"username": "", "password": ""}
            else:
                self.auth = self.global_auth

    def send(self):
        if isinstance(self.body, str):
            r = requests.request(
                url=self.base_url + self.path,
                method=self.method,
                params=self.params,
                headers=self.headers,
                # TODO: Beef up this logic to ensure a strict data type (binary/bytes?)
                data=self.body,
                auth=HTTPBasicAuth(self.auth["username"], self.auth["password"]),
            )
            return Response(
                status_code=r.status_code, headers=dict(r.headers), body=str(r.text)
            )
        else:
            r = requests.request(
                url=self.base_url + self.path,
                method=self.method,
                params=self.params,
                headers=self.headers,
                json=self.body,
                auth=HTTPBasicAuth(self.auth["username"], self.auth["password"]),
            )
            return Response(
                status_code=r.status_code, headers=dict(r.headers), body=str(r.text)
            )
