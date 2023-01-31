from .preprocessing import evaluate
from .models import Step
from .verify import *

from rich import print, print_json
import json


def make_requests(
    steps_data: dict, operation_schemas: dict, fail_fast: bool, verbose: bool
):

    base_url: str = steps_data["base_url"]

    # Set global auth if it exists in the step file
    global_auth: dict = None
    if "auth" in steps_data.keys():
        global_auth: dict = {}
        for key, value in steps_data["auth"].items():
            global_auth[key] = evaluate(value)
    else:
        global_auth = None

    # Get steps list
    steps_data: list = steps_data["steps"]

    # Create Global Steps List
    steps: dict = {}

    for s in steps_data:
        print(f"Step Name: {s['name']}")
        step = Step(s, steps)
        request = step.construct_request(base_url, global_auth)

        try:
            response_schema = operation_schemas[s["operation_id"]]["responses"][
                str(s["status_code"])
            ]
        except KeyError as e:
            print("[bold red]Response Validation Error[/bold red]")
            raise KeyError(
                f"Response code of {e} not found in responses for {s['operation_id']}"
            ) from e

        if "requestBody" in operation_schemas[s["operation_id"]].keys():
            verify_request_body(
                request.body, operation_schemas[s["operation_id"]]["requestBody"]
            )

        response = request.send()
        if verbose:
            if response.data:
                print("---Response---")
                print(f"Status Code: {response.status_code}")
                print_json(response.data)

        response_type = ""
        if (
            "type"
            in operation_schemas[s["operation_id"]]["responses"][
                str(s["status_code"])
            ].keys()
        ):
            response_type = operation_schemas[s["operation_id"]]["responses"][
                str(s["status_code"])
            ]["type"]

        if response_type == "object" or response_type == "array":
            response.data = json.loads(response.data)

        verify_response(response, s["status_code"], response_schema)
        if verbose:
            print("[bold green]--Step Verified--[/bold green]")

        steps[s["name"]] = {}
        steps[s["name"]]["response"] = response
