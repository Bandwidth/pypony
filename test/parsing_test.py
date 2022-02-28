"""This module contains tests for src/parsing.py.
"""

from prance import ValidationError
from src.parsing import parse_spec, parse_steps

from .fixtures import *
from prance.util.url import ResolutionError


def test_parse_valid_specs(valid_specs: list[str]):
    required_keys = ["openapi", "info", "paths", "components"]
    for valid_spec in valid_specs:
        parsed_spec = parse_spec(valid_spec)
        assert parsed_spec.keys() & required_keys == set(required_keys)


def test_parse_invalid_specs(invalid_specs: list[str]):
    for invalid_spec in invalid_specs:
        with pytest.raises((ValidationError, ResolutionError)):
            parse_spec(invalid_spec)

    with pytest.raises(FileNotFoundError):
        parse_spec("test/fixtures/specs/doesnt_exist_spec.yml")


def test_parse_valid_steps(valid_steps: list[str]):
    for valid_step in valid_steps:
        parsed_steps = parse_steps(valid_step)
        assert {"base_url", "paths"}.issubset(parsed_steps.keys())
