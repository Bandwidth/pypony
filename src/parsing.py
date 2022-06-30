# -*- coding: utf-8 -*-
"""parsing.py

This module contains functions for parsing the input file.
It will parse input files, returning a nested dictionary object.
If the input file is not valid, it will raise an exception.
"""

import os

import yaml
from jsonschema import validate, ValidationError
from openapi_spec_validator import validate_spec
from prance import ResolvingParser, ValidationError
from prance.util.url import ResolutionError
from ruamel.yaml.scanner import ScannerError as RuamelScannerError
from yaml.constructor import SafeConstructor
from yaml.scanner import ScannerError as PyYAMLScannerError


def parse_spec(spec_file_path: str) -> dict:
    """Parse OpenAPI spec file to a dictionary.

    Args:
        spec_file_path (str): Path to spec file.

    Returns:
        dict: Spec file parsed into a dictionary.

    Raises:
        ValidationError: If the spec file is not valid according to the OpenAPI spec.
        ResolutionError: If the spec file has refs cannot be resolved
        ruamel.yaml.scanner.ScannerError:
    """

    if not os.path.exists(spec_file_path):
        raise FileNotFoundError(f"Spec file '{spec_file_path}' not found")

    try:
        parser = ResolvingParser(spec_file_path)
        spec_dict = parser.specification
        validate_spec(spec_dict)
        return spec_dict
    except ValidationError as e:
        raise ValidationError(
            f"Spec file {spec_file_path} is not valid according to the OpenAPI specification"
        ) from e
    except ResolutionError as e:
        raise ResolutionError(
            f"Spec file {spec_file_path} has refs that cannot be resolved"
        )
    except RuamelScannerError as e:
        raise RuamelScannerError(
            f"Could not parse {spec_file_path} as a YAML file"
        ) from e


def parse_steps(step_file_path: str) -> dict:
    """Parse steps file to a dictionary.

    Args:
        step_file_path (str): Path to step file.

    Returns:
        dict: Step file parsed into a dictionary.

    Raises:
        FileNotFoundError: If the step file does not exist.
        yaml.scanner.ScannerError: If the step file is not valid YAML.
        JSONValidatorError: If the step file is not valid against the step file schema.
    """

    try:
        steps_schema_path = os.path.join(os.path.dirname(__file__), "steps_schema.yml")
        with open(steps_schema_path, "r") as step_schema_file:
            steps_schema = yaml.safe_load(step_schema_file.read())
    except FileNotFoundError as e:
        raise FileNotFoundError("Steps schema file not found") from e

    try:
        with open(step_file_path, "r") as step_file:
            # Drop support for datetime
            SafeConstructor.yaml_constructors[
                "tag:yaml.org,2002:timestamp"
            ] = SafeConstructor.yaml_constructors["tag:yaml.org,2002:str"]

            # Load the step file and validate it against the step file schema
            yaml_dict = yaml.safe_load(step_file)
            validate(yaml_dict, steps_schema)

    except ValidationError as e:
        raise ValidationError(f"Steps file has the following syntax errors: {e} ") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Steps file {step_file_path} not found") from e
    except PyYAMLScannerError as e:
        raise PyYAMLScannerError("Steps file is not valid YAML") from e

    return yaml_dict
