# -*- coding: utf-8 -*-
"""errors.py:

This module contains custom errors related to the models subpackage.
These errors mostly include exceptions related to resolving previous step and environment variable references in step files.
"""


class BaseContextError(Exception):
    """
    Raises when the base context of an expression is not either "env" or "steps".
    """
    def __init__(self, value):
        super().__init__(
            f"the base context must be either 'env' or 'steps', but found '{value}'"
        )


class EvaluationError(Exception):
    """
    Raises when the errors occur during expression evaluation.
    """
    def __init__(self, message):
        super().__init__(message)


class EnvironmentVariableError(Exception):
    """
    Raises when an environment variable is not found.
    """
    def __init__(self, value):
        super().__init__(f"environment variable {value} not found")


class InvalidExpressionError(Exception):
    """
    Raises when an expression is invalid.
    """
    def __init__(self, value):
        super().__init__(f"invalid expression: {value}")
