import pytest
from hamcrest import assert_that, is_, has_items, instance_of

from src.parsing import *
from src.preprocessing import *


class TestPreProcessing:
    """Class for basic unit testing of the preprocessing.py module"""

    steps_file_path = "./tests/fixtures/valid/steps/person_api.yml"
    spec_file_path = "./tests/fixtures/valid/specs/person_api.yml"

    steps = parse_steps_file(steps_file_path)
    spec, operation_schemas = parse_spec_file(steps, spec_file_path)

    def test_get_operation_coverage(self):
        step_coverage, spec_coverage = get_operation_coverage(self.steps, self.spec)
        assert_that(step_coverage == spec_coverage)

    def test_check_operation_coverage(self):
        check_operation_coverage(self.steps, self.spec)

    def test_evaluate_expression(self):
        evaluated_empty_expression = evaluate(None)
        assert_that(evaluated_empty_expression, is_(None))

        evaluated_env_var_expression = evaluate("${{ env.PYPONY_RELEASE_VERSION }}")
        assert_that(evaluated_env_var_expression, is_("0.0.0"))

        # TODO: More tests for evaluate()
        # evaluated_steps_expression = evaluate("${{ steps.someStep }}", {})
