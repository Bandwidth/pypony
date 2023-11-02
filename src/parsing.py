import os
import json

import yaml
from jsonschema import validate, ValidationError
from json_ref_dict import materialize, RefDict
from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPIValidationError
from rich import print

from .errors import *


def parse_steps_file(step_file_path: str) -> dict:
    """Parse a .yml steps file and convert it to a python dictionary

    Args:
        step_file_path (str): Relative path to steps file

    Raises:
        FileNotFoundError: Step file not found
        ValidationError: Step file not valid

    Returns:
        dict: Step file converted to a python dictionary
    """
    try:
        steps_schema_path = os.path.join(os.path.dirname(__file__), "steps_schema.yml")
        with open(steps_schema_path, "r") as step_schema_file:
            steps_schema = yaml.safe_load(step_schema_file.read())
    except FileNotFoundError as e:
        raise FileNotFoundError("Steps schema file not found") from e

    try:
        with open(step_file_path, "r") as step_file:
            steps = yaml.safe_load(step_file.read())
            validate(instance=steps, schema=steps_schema)

    except ValidationError as e:
        raise ValidationError(
            f"Steps file has the following syntax errors: {e.message} "
        ) from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Steps file {step_file_path} not found") from e

    print("[bold green]--Successfully Validated Steps File--[/bold green]")
    return steps


def parse_spec_file(steps: dict, spec_file_path: str) -> tuple:
    """Parse a valid OpenAPI document into a python dictionary

    Args:
        spec_file_path (str): Relative path to OpenAPI spec file

    Raises:
        OpenAPIValidationError: Invalid API Definition
        FileNotFoundError: Spec file not found
        UnsupportedSchemaError: Schema not supported

    Returns:
        tuple: Returns a tuple containing two dictionaries - the parsed API spec and
            a dictionary with all of the openapi operations for quick reference
    """
    try:
        spec = materialize(RefDict(spec_file_path))
        validate_spec(spec)
    except OpenAPIValidationError as e:
        raise OpenAPIValidationError(
            f"API Spec file has the following syntax errors: {e.message} "
        ) from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"API Spec file {spec_file_path} not found") from e

    # Get list of steps operationIds
    steps_opertaion_id_list = []
    for step in steps["steps"]:
        steps_opertaion_id_list.append(step["operation_id"])

    # Create operation schemas dict for easier parsing
    operation_schemas: dict = {}
    for path in spec["paths"]:
        for method in spec["paths"][path]:
            op_id = spec["paths"][path][method]["operationId"]
            if op_id in steps_opertaion_id_list:
                operation = spec["paths"][path][method]
                operation_schemas[op_id] = {}

                # Parse and Validate Request Bodies
                if "requestBody" in operation.keys():
                    # TODO: Support multiple content types if one of them is JSON
                    if len(operation["requestBody"]["content"]) > 1:
                        if (
                            "application/json"
                            not in operation["responses"][status_code]["content"]
                        ):
                            raise UnsupportedSchemaError(
                                f"There are too many request body content types for"
                                f" the operation: {op_id}"
                            )
                    if "application/json" in operation["requestBody"]["content"].keys():
                        operation_schemas[op_id]["requestBody"] = operation[
                            "requestBody"
                        ]["content"]["application/json"]["schema"]
                    elif (
                        "application/octet-stream"
                        in operation["requestBody"]["content"].keys()
                    ):
                        operation_schemas[op_id]["requestBody"] = operation[
                            "requestBody"
                        ]["content"]["application/octet-stream"]["schema"]
                    else:
                        raise UnsupportedSchemaError(
                            f"request body content type: "
                            f"{list(operation['requestBody']['content'].keys())[0]}"
                            f" unsupported for the operation: {op_id}"
                        )

                # Parse and Validate Response Bodies
                operation_schemas[op_id]["responses"] = {}
                for status_code in operation["responses"].keys():
                    if "content" in operation["responses"][status_code].keys():
                        # TODO: Support multiple content types if one of them is JSON
                        if len(operation["responses"][status_code]["content"]) > 1:
                            if (
                                "application/json"
                                not in operation["responses"][status_code]["content"]
                            ):
                                raise UnsupportedSchemaError(
                                    f"There are too many response body content types for"
                                    f" the operation: {op_id}"
                                )
                        if (
                            "application/json"
                            in operation["responses"][status_code]["content"].keys()
                        ):
                            operation_schemas[op_id]["responses"][
                                status_code
                            ] = operation["responses"][status_code]["content"][
                                "application/json"
                            ][
                                "schema"
                            ]
                        elif (
                            "application/octet-stream"
                            in operation["responses"][status_code]["content"].keys()
                        ):
                            operation_schemas[op_id]["responses"][
                                status_code
                            ] = operation["responses"][status_code]["content"][
                                "application/octet-stream"
                            ][
                                "schema"
                            ]
                        else:
                            raise UnsupportedSchemaError(
                                f"response body content type: "
                                f"{list(operation['responses'][status_code]['content'].keys())[0]}"
                                f" unsupported for the operation: {op_id}"
                            )
                    else:
                        operation_schemas[op_id]["responses"][status_code] = operation[
                            "responses"
                        ][status_code]

    print("[bold green]--Successfully Validated Spec File--[/bold green]")
    return spec, operation_schemas
