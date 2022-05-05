# -*- coding: utf-8 -*-
"""response.py

Response is generated once a request gets a response back from the server.
"""

from dataclasses import dataclass

import requests
from addict import Dict


@dataclass
class Response:
    """
    Stores the response sent back to the server.
    """

    __response: requests.Response

    def __getattr__(self, item):
        if item == "body":
            if 'application/json' in self.__response.headers['Content-Type']:
                body = self.__response.json()
            else:
                body = self.__response.content
            return Dict(body) if isinstance(body, dict) else body

        return getattr(self.__response, item)
