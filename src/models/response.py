class Response:
    def __init__(
        self,
        status_code: int,
        headers: dict,
        data: dict,
    ):
    
        self.status_code = status_code
        self.headers = headers
        self.data = data
