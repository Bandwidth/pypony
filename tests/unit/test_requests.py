import pytest

from src.parsing import parse_steps_file, parse_spec_file
from src.requests import make_requests


class TestRequests:
    """Class for basic unit testing of the requests.py module"""

    steps_file_path = "./tests/fixtures/valid/steps/person_api.yml"
    spec_file_path = "./tests/fixtures/valid/specs/person_api.yml"

    valid_test_steps = parse_steps_file(steps_file_path)
    valid_test_spec, operationSchemas = parse_spec_file(valid_test_steps, spec_file_path)

    # skip test
    @pytest.mark.skip(reason="Not testable at the moment")
    def test_make_requests_with_valid_steps_and_spec(self):
        make_requests(self.valid_test_steps, self.valid_test_spec, False, False)
