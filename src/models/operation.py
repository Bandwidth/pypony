# -*- coding: utf-8 -*-
"""operation.py:

Encapsulates operation data from the step file, including name, request, response, and schema for easy access.
"""

from dataclasses import dataclass

from jschon.jsonschema import Scope

from .request import Request
from .response import Response
from .schema import Schema


@dataclass
class Operation:
    """
    Operations object manages request, response, and schema.
    """

    name: str
    request: Request = None
    response: Response = None
    schema: Schema = None

    def verify(self) -> Scope:
        """
        Verify the response against the schema.

        Returns:
            Evaluate the response body and return the complete evaluation result tree.
        """
        return self.schema.evaluate(self.response.json())
