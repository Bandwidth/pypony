from rich import print

class UndocumentedOperationError(BaseException):
    """
    Raised when the step file contains operations that are not documented in the OpenAPI spec.
    This error will halt further execution of the action.
    """

    def __init__(self, undocumented: set[str]):
        super().__init__(
            print(f"The following operations from the steps file are undocumented: [bold red]{undocumented}[/bold red]")
        )


class InsufficientCoverageError(BaseException):
    """
    Raised if the step file does not sufficiently cover the OpenAPI spec according the the coverage threshold.
    If a coverage threshold given in the step file, this error will halt further execution of the action.
    """

    def __init__(
        self, achieved_coverage: float, target_coverage: float, uncovered: set[str]
    ):
        super().__init__(
            print(f'''The operation coverage is [bold red]{achieved_coverage}[/bold red]
but the target is [green]{target_coverage}[/green].\n
The following operations are uncovered: [bold red]{uncovered}[/bold red]''')
        )


class InvalidFileError(BaseException):
    """
    Raised when you pass in an API spec file that is not JSON or YAML
    """
    def __init__(self, extension):
        super().__init__(
            print(f"Incorrect type for the API Spec file. Only [green]JSON[/green] and [green]YAML[/green] are supported. [bold red]{extension}[/bold red] supplied.")
        )


class BaseContextError(Exception):
    """
    Raises when the base context of an expression is not either "env" or "steps".
    """
    def __init__(self, value):
        super().__init__(
            f"The base context must be either 'env' or 'steps', but found [bold red]'{value}'[/bold red]"
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
