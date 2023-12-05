import pytest
from hamcrest import assert_that, is_, has_items, instance_of

from src.validate import *


class TestValidate:
    """Class for basic unit testing of the validate.py module"""

    steps_file_path = "./tests/fixtures/valid/steps/person_api.yml"
    spec_file_path = "./tests/fixtures/valid/specs/person_api.yml"

    @pytest.mark.skip(reason="Need to test against a mock API")
    def test_validate(self):
        validate(self.steps_file_path, self.spec_file_path, False, False)
