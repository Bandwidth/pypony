import pytest
from hamcrest import assert_that, is_, has_items, instance_of

from rich import inspect

from src.parsing import *

class TestParsing:
    """Class for basic unit testing of the parsing.py module
    """
    steps_file_path="./tests/fixtures/valid/steps/person_api.yml"
    spec_file_path = "./tests/fixtures/valid/specs/person_api.yml"

    invalid_steps_missing_operation_id_file_path="./tests/fixtures/invalid/steps/missing_property.yml"
    invalid_spec_missing_openapi_property_file_path = "./tests/fixtures/invalid/specs/invalid_spec_1.yml"
   
    def test_parse_steps_file_with_valid_steps(self):
        """Ensure a step file is parsed correctly
        """
        steps = parse_steps_file(self.steps_file_path)
        
        assert_that(steps, is_(instance_of(dict)))
        assert_that(steps, has_items('coverage_threshold', 'base_url', 'steps'))
        assert_that(steps['coverage_threshold'], is_(instance_of(float)))
        assert_that(steps['base_url'], is_(instance_of(str)))
        assert_that(steps['steps'], is_(instance_of(list)))

        assert_that(steps['steps'][0], has_items('name', 'operation_id', 'method', 'path', 'headers', 'body', 'auth', 'status_code'))
        assert_that(steps['steps'][0]['name'], is_(instance_of(str)))
        assert_that(steps['steps'][0]['operation_id'], is_(instance_of(str)))
        assert_that(steps['steps'][0]['method'], is_(instance_of(str)))
        assert_that(steps['steps'][0]['path'], is_(instance_of(str)))
        assert_that(steps['steps'][0]['headers'], is_(instance_of(dict)))
        assert_that(steps['steps'][0]['body'], is_(instance_of(dict)))
        assert_that(steps['steps'][0]['auth'], is_(instance_of(dict)))
        assert_that(steps['steps'][0]['status_code'], is_(instance_of(int)))

        assert_that(steps['steps'][1], has_items('name', 'operation_id', 'method', 'path', 'headers', 'auth', 'status_code'))

    def test_parse_steps_file_with_missing_operation_id(self):
        """Ensure that a missing required property raises a ValidationError
            ValidationError comes from the jsonschema library
        """
        with pytest.raises(ValidationError) as e:
            invalid_steps = parse_steps_file(self.invalid_steps_missing_operation_id_file_path)

    def test_parse_valid_spec_file(self):
        """Ensure an OpenAPI document is parsed correctly
        """
        spec, operation_schemas = parse_spec_file(self.spec_file_path)
        assert_that(spec, is_(instance_of(dict)))
        # TODO: More tests to assert children are properly formatted
        assert_that(operation_schemas, is_(instance_of(dict)))
        # TODO: More tests

    def test_parse_invalid_spec_file(self):
        """Ensure an OpenAPI document is parsed correctly
            OpenAPIValidationError comes from openapi_spec_validator library
        """
        with pytest.raises(OpenAPIValidationError):
            spec, operation_schemas = parse_spec_file(self.invalid_spec_missing_openapi_property_file_path)
