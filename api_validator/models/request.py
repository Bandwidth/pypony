# -*- coding: utf-8 -*-
"""request.py

Request will be sent off to a server to request or query some resource.
"""

from addict import Dict

from api_validator.models import Context

context = Context()


class Request:
    """
    Request object includes method, url, params, body, headers, and auth data.
    """
    def __init__(
        self,
        method: str,
        url: str,
        params: dict = None,
        body: dict = None,
        headers: dict = None,
        auth: dict = None,
    ):
        self.method = method
        self.url = url
        self.params = params
        self.body = body
        self.headers = headers
        self.auth = auth

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = Dict(value)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = Dict(value)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = Dict(value)

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        self._auth = Dict(value if value else {"username": "", "password": ""})

    def evaluate_all(self) -> None:
        """
        Evaluates url, params, body, and header in-place.

        Expressions can be either simple or nested:

            /users/${{ steps.createUser.response.body.id }}
            /users/${{ steps.createUser.response.body.id }}/orders/${{ steps.getOrders.response.body[0].id }}
        """

        self.url = context.evaluate(self.url)

        # Evaluate all Dict object
        for name in ("params", "body", "headers", "auth"):
            attr = self.__getattribute__(name)
            self.__setattr__(name, context.evaluate(attr))
