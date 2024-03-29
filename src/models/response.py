from typing import Union


class Response:
    def __init__(
        self,
        status_code: int,
        headers: dict,
        body: Union[dict, str],
    ):

        self.status_code = status_code
        self.headers = headers
        self.body = body
