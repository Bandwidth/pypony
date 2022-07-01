import requests
from requests.auth import HTTPBasicAuth
from rich import inspect


from src.models.response import Response

class Request:
    def __init__(
        self,
        base_url,
        path,
        params,
        headers,
        global_auth,
        auth,
        body
    ):
        self.base_url = base_url
        self.path=path,
        self.params=params,
        self.headers=headers,
        self.global_auth=global_auth,
        self.auth=auth,
        self.body=body

    def send():
        return Response
