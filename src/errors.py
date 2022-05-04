# -*- coding: utf-8 -*-
"""errors.py

This module contains custom errors for the API validator.
Often, these errors are raised when a library gives an error with a difficult to read message.
These errors will nicely format these error messages for logging and stack traces.
"""

# Import errors from models subpackage
from .models.errors import *

# For type hints
from .models import Response


class UndocumentedOperationError(BaseException):
    """
    Raised when the step file contains endpoints that are not documented in the OpenAPI spec.
    This error will halt further execution of the action.
    """

    def __init__(self, undocumented: set[str]):
        super().__init__(
            f"""The following operations are undocumented:
    {undocumented}"""
        )


class InsufficientCoverageError(BaseException):
    """
    Raised the step file does not sufficiently cover the OpenAPI spec according the the coverage threshold.
    If a coverage threshold given in the step file, this error will halt further execution of the action.
    """

    def __init__(
        self, achieved_coverage: float, target_coverage: float, uncovered: set[str]
    ):
        super().__init__(
            f"""The operation coverage is {achieved_coverage} but the target is {target_coverage}.
    The following operations are uncovered: {uncovered}"""
        )


class ResponseMatchError(BaseException):
    """
    Raised when a response does not match any of the expected responses in the OpenAPI spec according to status code.
    This error will halt further execution of the action.
    """

    def __init__(self, statuses: list, step: Response):
        super().__init__(
            f"""Cannot find a matching response in the specification.
    Expected possible responses:
        {', '.join(list(statuses))}
    Actual response:
        {step.status_code}"""
        )


class ResponseValidationError(BaseException):
    """
    Raised when the structure of a response does not match the expected schema in the OpenAPI spec.
    This error will halt further execution of the action.
    """

    def __init__(self, errors: list, url: str, method: str, status_code: int):
        super().__init__(
            f"""Response is not valid against the schema at:
    {url}:
        {method}:
            {status_code}:
                {list(map(lambda x: {x['keywordLocation']: x['error']}, errors))}"""
        )


class JSONValidatorError(BaseException):
    """
    Raised when the structure of a JSON does not match the expected JSON schema.
    This error will halt further execution of the action.
    """

    def __init__(self, errors: list[dict[str, str]]):
        super().__init__(
            "\n".join(
                [
                    f"""{error['instanceLocation']}\n  {error['error']}"""
                    for error in errors
                ]
            )
        )
