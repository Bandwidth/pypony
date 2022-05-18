# -*- coding: utf-8 -*-
"""validate.py

This module contains the primary code for the package.
Using the parsed OpenAPI specs and step files, it will create API requests and
validate the responses.
"""
import traceback

import requests
from rich import print, print_json
from jschon import create_catalog
from openapi_schema_to_json_schema import to_json_schema
from requests.auth import HTTPBasicAuth

from .errors import (
    InsufficientCoverageError,
    ResponseMatchError,
    ResponseValidationError,
    UndocumentedOperationError,
)
from .models import Context, Request, Response, Schema, Step
from .parsing import parse_spec, parse_steps
from .preprocessing import get_operation_coverage

# Global variable storing all runtime contexts (initialize once)
context = Context()


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
    print("---Parsing spec file---")
    spec_data = parse_spec(spec_file_path)

    # Parse step file
    print("---Parsing step file---")
    steps_data = parse_steps(step_file_path)

    return spec_data, steps_data


def check_operation_coverage(spec_data: dict, steps_data: dict):
    """
    Checks the operation coverage of the step file against the OpenAPI spec.

    Args:
        spec_data (dict): The parsed OpenAPI spec
        steps_data (dict): The parsed step file
    Raises:
        UndocumentedOperationError:
    """

    operation_coverage = get_operation_coverage(spec_data, steps_data)

    # If any undocumented operations, immediately halt
    if operation_coverage.has_undocumented_operations():
        raise UndocumentedOperationError(operation_coverage.undocumented)

    # Check if operation coverage meets threshold
    if "coverage_threshold" in steps_data:
        target_coverage: float = steps_data["coverage_threshold"]
        achieved_coverage = operation_coverage.proportion_covered()

        if achieved_coverage < target_coverage:
            raise InsufficientCoverageError(
                achieved_coverage, target_coverage, operation_coverage.uncovered
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

    print('---Validating APIs---')

    # Set base url
    base_url: str = steps_data["base_url"]

    # Set global auth if it exists in the step file
    global_auth: dict = {}
    if 'auth' in steps_data.keys():
        global_auth: dict = steps_data["auth"]

    # Get steps list
    steps: list = steps_data["steps"]

    # Create responses dict for easier parsing
    operation_responses: dict = {}
    for path in spec_data['paths']:
        for method in spec_data['paths'][path]:
            op_id = spec_data['paths'][path][method]['operationId']
            operation_responses[op_id] = spec_data['paths'][path][method]['responses']

    # Go through each step
    step_data: dict
    for step_data in steps:
        try:
            # Get step name
            step_name = step_data.pop("name")

            # Create Request object
            path_url = step_data.pop("url")
            request = Request(url=(base_url + path_url), global_auth=global_auth, **step_data)
            
            # TODO: something isnt right here - setting request body as application/xml
            #  in the spec but json in the step doesnt cause a failure
            # Evaluate expressions
            request.evaluate_all()

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
            status_code = step.response.status_code

            # Fetch schema
            try:
                schema = to_json_schema(operation_responses[step_data['operation_id']][str(step_data['status_code'])])
            except (AttributeError, KeyError):
                raise ResponseMatchError(
                    operation_responses[step_data['operation_id']].keys(),
                    step.response,
                )

            # delete the $schema key that `to_json_schema` creates, it causes issues in the Schema class
            try:
                del schema['$schema']
            except KeyError:
                pass

            # Save the step to further use
            context.add_steps(step)

            # Verify the response
            if 'application/json' in schema['content'].keys():
                step.schema = Schema(schema)
                verification_result = step.verify()
            else:
                if verbose:
                    print('The response schema Content-Type for this endpoint is not supported.'
                          '\nThis response will not be validated.')

            # TODO: make this nicer using a rich table
            if verbose: 
                print(f'Step: {step_name}')
                print('--------------------')
                print('Request:')
                print(f'{request.method} {request.url}')
                print(f'Authentication: {request.auth}')
                print(f'Body:')
                print_json(data=request.body, indent=4)
                print(f'Headers: {request.headers}')
                print(f'Parameters: {request.params}')
                print('--------------------')
                print('Response:')
                print(f'HTTP {response.status_code} {response.reason}')
                if type(response.body) == bytes:
                    print(f'Body size: {len(response.body)} bytes')
                else:
                    print('Body:')
                    print_json(data=response.body, indent=4)
                print('--------------------\n\n')


            if not verification_result.valid:
                raise ResponseValidationError(
                    errors=verification_result.output('basic')["errors"],
                    url=path_url,
                    method=step_data['method'],
                    status_code=status_code,
                )

        except BaseException as e:
            if fail_fast:
                raise e

            if verbose:
                print(f'[red]{traceback.format_exc()}[/red]')
            else:
                print(f'[bold red]{str(e)}[/bold red]')


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

    create_catalog("2020-12")

    # Parse spec and step files
    spec_data, steps_data = parse_spec_steps(spec_file_path, step_file_path)

    # TODO: This is broken. Outputs `paths' and exits
    #  the reason for this is that the original code looked for a `paths` dict in the spec and steps.
    #  with the overhaul of the schema to use operations, this logic was broken 
    #  i think the best path forward is to compare operations instead of path coverage since paths can have multiple operations
    # TODO: Refactor to `check_operation_coverage`
    # Check operation coverage
    check_operation_coverage(spec_data, steps_data)

    # Make requests
    make_requests(spec_data, steps_data, fail_fast, verbose)
