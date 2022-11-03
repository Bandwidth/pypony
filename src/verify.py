from jsonschema import validate, ValidationError
from rich import print


def verify_request_body(request, schema):
    try:
        validate(instance=request, schema=schema)
    except ValidationError as e:
        print("[bold red]--Request Validation Failed--[/bold red]")
        raise ValidationError("There was an issue with your request body.") from e
    return


def verify_response(response, status_code, schema):
    if response.status_code != status_code:
        print("[bold red]--Response Validation Failed--[/bold red]")
        raise ValidationError("HTTP Status Code does not match the expected value from the step file.")
    else:
        try:
            validate(instance=response.data, schema=schema)
        except ValidationError as e:
            print("[bold red]--Response Validation Failed--[/bold red]")
            print(e)
            raise ValidationError("There was an issue with the response from the API.")
    return
