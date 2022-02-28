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
            body = self.__response.json()
            return Dict(body) if isinstance(body, dict) else body

        return getattr(self.__response, item)