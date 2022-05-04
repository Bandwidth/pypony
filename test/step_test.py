import json

from src.errors import JSONValidatorError
from jsonschema import ValidationError
from src.parsing import parse_steps
from yaml.scanner import ScannerError
from jschon import JSONSchema

from .fixtures import *

# Load JSON catalog and steps schema
#create_catalog("2020-12", default=True)

# with open("src/steps_schema.yml", "r") as f:
#     schema = JSONSchema(json.load(f))


def test_parse_valid_steps(valid_steps: list[str]):
    for vs in valid_steps:
        try:
            parse_steps(vs)
        except Exception as e:
            pytest.fail("Valid step file was deemed invalid")


def test_parse_invalid_steps(invalid_schema_steps: list[str]):
    for vs in invalid_schema_steps:
        with pytest.raises(ValidationError):
            parse_steps(vs)


def test_parse_invalid_yaml(invalid_scanner_steps: list[str]):
    for vs in invalid_scanner_steps:
        with pytest.raises(ScannerError):
            parse_steps(vs)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_steps("test/fixtures/steps/doesnt_exist_steps.yml")
