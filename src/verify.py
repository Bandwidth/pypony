from jsonschema import validate, ValidationError
from rich import print
from typing import Union

from .models import Response


def verify_request_body(request_body: Union[dict, str], schema: dict):
    """Verify that the request body matches the schema provided in the step file"""

    try:
        validate(instance=request_body, schema=schema)
    except ValidationError as e:
        print("[bold red]--Request Validation Failed--[/bold red]")
        raise ValidationError("There was an issue with your request body.") from e
    return


def verify_response(response: Response, status_code: int, schema: dict):
    """Verify that the response matches the schema provided in the step file"""

    if response.status_code != status_code:
        print("[bold red]--Response Validation Failed--[/bold red]")
        raise ValidationError(
            "HTTP Status Code does not match the expected value from the step file."
        )
    else:
        try:
            validate(instance=response.body, schema=schema)
        except ValidationError as e:
            print("[bold red]--Response Validation Failed--[/bold red]")
            print(e)
            raise ValidationError("There was an issue with the response from the API.")
    return
