# -*- coding: utf-8 -*-
"""action.py

This module contains the primary code for the GitHub Action.
Using the parsed OpenAPI specs and step files, it will create API requests and
validate the responses.
"""
import os
import traceback

import requests
from actions_toolkit import core
from dotenv import load_dotenv
from jschon import create_catalog
from jschon.jsonschema import OutputFormat
from openapi_schema_to_json_schema import to_json_schema
from requests.auth import HTTPBasicAuth

from .errors import (
    InsufficientCoverageError,
    ResponseMatchError,
    ResponseValidationError,
    UndocumentedEndpointError,
)
from .models import Context, Request, Response, Schema, Step
from .parsing import parse_spec, parse_steps
from .preprocessing import get_endpoint_coverage

# Global variable storing all runtime contexts (initialize once)
context = Context()

# Load dotenv
load_dotenv()


def parse_spec_steps(spec_file_path: str, step_file_path: str) -> tuple[dict, dict]:
    """
    Parses the OpenAPI spec and step files and return each of them

    Args:
        spec_file_path (str): The path to the OpenAPI spec file
        step_file_path (str): The path to the step file
    Returns:
        A 2-tuple of dictionaries, containing the parsed OpenAPI spec and step files
    Raises:
        FileNotFoundError: If the spec or step file does not exist
        ValidationError: If the spec file is not valid according to the OpenAPI standard
        ScannerError: If the step file is not valid YAML
        JSONValidatorError: If the step file instance is not valid according to the JSON schema
    """

    # Parse OpenAPI specification file
    core.start_group("Parsing spec file")
    spec_data = parse_spec(spec_file_path)
    core.end_group()

    # Parse step file
    core.start_group("Parsing step file")
    steps_data = parse_steps(step_file_path)
    core.end_group()

    return spec_data, steps_data


def check_endpoint_coverage(spec_data: dict, steps_data: dict):
    """
    Checks the endpoint coverage of the step file against the OpenAPI spec.

    Args:
        spec_data (dict): The parsed OpenAPI spec
        steps_data (dict): The parsed step file
    Raises:
        UndocumentedEndpointError:
    """

    endpoint_coverage = get_endpoint_coverage(spec_data, steps_data)

    # If any undocumented endpoints, immediately halt
    if endpoint_coverage.has_undocumented_endpoints():
        raise UndocumentedEndpointError(endpoint_coverage.undocumented)

    # Check if endpoint coverage meets threshold
    if "coverage_threshold" in steps_data:
        target_coverage: float = steps_data["coverage_threshold"]
        achieved_coverage = endpoint_coverage.proportion_covered()

        if achieved_coverage < target_coverage:
            raise InsufficientCoverageError(
                achieved_coverage, target_coverage, endpoint_coverage.uncovered
            )


def make_requests(spec_data: dict, steps_data: dict, fail_fast: bool, verbose: bool):
    """
    Given a parsed OpenAPI spec and step file, make requests and validate responses.

    Args:
        spec_data (dict): The parsed OpenAPI spec
        steps_data (dict): The parsed step file
        fail_fast (bool): Whether to exit immediately if exception raised
        verbose (bool): Whether to output stacktrace
    Raises:
        ResponseMatchError: If the response does not match the expected response according to status code
        ResponseValidationError: If the response does not match the expected response according to schema
    """

    core.info('Validating APIs')

    # Create requests
    base_url: str = steps_data["base_url"]
    paths: dict = steps_data["paths"]

    # Go through each path in the steps
    path_value: dict
    for path_key, path_value in paths.items():
        core.start_group(path_key)

        # Go through each method in each path
        method_value: dict
        for method_name, method_value in path_value.items():
            # Store steps of current method
            context.clear_steps()

            # Get steps YAML from file
            method_steps: list = method_value["steps"]

            # Go through each step in each method
            step_data: dict
            for step_data in method_steps:
                try:
                    # Get step name
                    step_name = step_data.pop("name")
                    core.info(step_name)

                    # Create Request object
                    path_url = step_data.pop("url")
                    request = Request(url=(base_url + path_url), **step_data)

                    # Evaluate expressions
                    request.evaluate_all()

                    core.info('  Request:')
                    core.info(f'    {request.method} {request.url}')
                    core.info(f'      Authentication: {request.auth}')
                    core.info(f'      Body: {request.body}')
                    core.info(f'      Headers: {request.headers}')
                    core.info(f'      Parameters: {request.params}')

                    # Create Step object
                    step = Step(step_name, request)

                    # Send the request
                    step.response = Response(
                        requests.request(
                            method=request.method,
                            url=request.url,
                            params=request.params.to_dict(),
                            headers=request.headers.to_dict(),
                            json=request.body.to_dict(),
                            auth=HTTPBasicAuth(**request.auth),
                        )
                    )

                    response = step.response

                    core.info('  Response:')
                    core.info(f'    HTTP {response.status_code} {response.reason}')
                    core.info(f'    Body: {response.body}')
                    core.info('')

                    status_code = step.response.status_code

                    # Fetch schema
                    try:
                        schema = to_json_schema(
                            spec_data.get("paths")
                                .get(path_key)
                                .get(method_name)
                                .get("responses")
                            .get(str(status_code))
                            .get("content")
                            .get("application/json")
                            .get("schema")
                        )
                        step.schema = Schema(schema)
                    except AttributeError:
                        raise ResponseMatchError(
                            spec_data.get("paths")
                            .get(path_key)
                            .get(method_name)
                            .get("responses")
                            .keys(),
                            step.response,
                        )

                    # Save the step to further use
                    context.add_steps(step)

                    # Verify the response
                    verification_result = step.verify()
                    if not verification_result.valid:
                        raise ResponseValidationError(
                            errors=verification_result.output(OutputFormat.BASIC)["errors"],
                            url=path_url,
                            method=method_name,
                            status_code=status_code,
                        )

                except BaseException as e:
                    if fail_fast:
                        raise e

                    if verbose:
                        core.warning(traceback.format_exc(), title=e.__class__.__name__)
                    else:
                        core.warning(str(e), title=e.__class__.__name__)

    core.end_group()


def verify_api(spec_file_path: str, step_file_path: str, fail_fast: bool = False, verbose: bool = False):
    """
    This is the main function of the API verifier.
    It parses the OpenAPI spec and step files, measures coverage, makes requests, and validates responses.
    If this method completes without raising any exceptions, the API is considered valid.

    Args:
        spec_file_path (str): The path to the OpenAPI spec file
        step_file_path (str): The path to the step file
        fail_fast (bool): Whether to exit immediately if exception raised
        verbose (bool): Whether to output stacktrace
    """

    create_catalog("2020-12", default=True)

    # Parse spec and step files
    spec_data, steps_data = parse_spec_steps(spec_file_path, step_file_path)

    # Check endpoint coverage
    check_endpoint_coverage(spec_data, steps_data)

    # Make requests
    make_requests(spec_data, steps_data, fail_fast, verbose)
