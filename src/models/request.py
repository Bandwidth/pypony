import requests
from requests.auth import HTTPBasicAuth
from rich import inspect


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
        body: dict
    ):
        self.base_url = base_url
        self.method = method
        self.path=path
        self.params=params
        self.headers=headers
        self.global_auth=global_auth
        self.auth=auth
        self.body=body
        
        if not self.auth:
            if not self.global_auth:
                self.auth = {'username': '', 'password': ''}
            else: 
                self.auth=self.global_auth

    def send(self):
        r = requests.request(
                url=self.base_url + self.path,
                method=self.method,
                params=self.params,
                headers=self.headers,
                json=self.body,
                auth=HTTPBasicAuth(self.auth['username'], self.auth['password']),
        )
        return Response(
            status_code=r.status_code,
            headers=r.headers,
            data=r.json()
        )
