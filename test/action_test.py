import io
import os
from contextlib import redirect_stdout

import prance
import pytest

from api_validator.action import verify_api
from api_validator.errors import (
    UndocumentedEndpointError,
    InsufficientCoverageError,
    ResponseMatchError,
    ResponseValidationError,
)
from yaml.scanner import ScannerError
from ruamel.yaml.scanner import ScannerError as RuamelScannerError
from prance.util.url import ResolutionError


def test_make_requests():
    os.environ["SERVER_ENV"] = "development"

    verify_api(
        "test/fixtures/specs/valid/localhost.spec.yml",
        "test/fixtures/steps/valid/localhost.step.yml",
    )


def test_spec_file_not_found_error():
    spec_file_path = os.path.join(
        "test", "fixtures", "specs", "invalid", "what_is_this.spec.yml"
    )
    assert not os.path.exists(spec_file_path)

    step_file_path = os.path.join(
        "test", "fixtures", "steps", "valid", "localhost.step.yml"
    )
    assert os.path.exists(step_file_path)

    with pytest.raises(FileNotFoundError):
        verify_api(spec_file_path, step_file_path)


def test_step_file_not_found_error():
    spec_file_path = os.path.join(
        "test", "fixtures", "specs", "valid", "localhost.spec.yml"
    )
    assert os.path.exists(spec_file_path)

    step_file_path = os.path.join(
        "test", "fixtures", "steps", "invalid", "what_is_this.step.yml"
    )
    assert not os.path.exists(step_file_path)

    with pytest.raises(FileNotFoundError):
        verify_api(spec_file_path, step_file_path)


def test_spec_validation_error():
    with pytest.raises(prance.ValidationError):
        verify_api(
            os.path.join("test", "fixtures", "specs", "invalid", "invalid_spec1.yml"),
            os.path.join("test", "fixtures", "specs", "valid", "valid_spec1.yml"),
        )


def test_step_scanner_error():
    with pytest.raises(ScannerError):
        verify_api(
            os.path.join("test", "fixtures", "specs", "valid", "localhost.spec.yml"),
            os.path.join(
                "test", "fixtures", "steps", "invalid", "scanner", "invalid_steps1.yml"
            ),
        )


def test_nullable_types():
    verify_api(
        os.path.join("test", "fixtures", "specs", "valid", "jservice.spec.yml"),
        os.path.join("test", "fixtures", "steps", "valid", "jservice.steps.yml"),
    )


def test_undocumented_endpoints():
    with pytest.raises(UndocumentedEndpointError):
        verify_api(
            os.path.join(
                "test", "fixtures", "specs", "valid", "localhost_undocumented.spec.yml"
            ),
            os.path.join("test", "fixtures", "steps", "valid", "localhost.step.yml"),
        )


def test_insufficient_endpoint_coverage():
    with pytest.raises(InsufficientCoverageError):
        verify_api(
            os.path.join("test", "fixtures", "specs", "valid", "coverage_spec.yml"),
            os.path.join(
                "test",
                "fixtures",
                "steps",
                "valid",
                "coverage_steps_all_documented.yml",
            ),
        )


def test_response_validation_error():
    with pytest.raises(ResponseValidationError):
        verify_api(
            os.path.join(
                "test", "fixtures", "specs", "valid", "jservice_incorrect1.spec.yml"
            ),
            os.path.join("test", "fixtures", "steps", "valid", "jservice.steps.yml"),
            fail_fast=True
        )


def test_response_match_error():
    with pytest.raises(ResponseMatchError):
        verify_api(
            os.path.join(
                "test", "fixtures", "specs", "valid", "jservice_incorrect2.spec.yml"
            ),
            os.path.join("test", "fixtures", "steps", "valid", "jservice.steps.yml"),
            fail_fast=True
        )


def test_ruamel_scanner_error():
    with pytest.raises(RuamelScannerError):
        # Setup.py cannot be parsed as YAML (because it isn't), so we get a RuamelScannerError
        verify_api(
            os.path.join("setup.py"),
            os.path.join("test", "fixtures", "steps", "valid", "jservice.steps.yml"),
        )


def test_resolution_error():
    with pytest.raises(ResolutionError):
        verify_api(
            os.path.join("test", "fixtures", "specs", "invalid", "missing_refs.yml"),
            os.path.join("test", "fixtures", "steps", "valid", "jservice.steps.yml"),
        )


def test_fail_fast_stdout():
    f = io.StringIO()
    with redirect_stdout(f):
        verify_api(
            os.path.join(
                "test", "fixtures", "specs", "valid", "jservice_incorrect1.spec.yml"
            ),
            os.path.join("test", "fixtures", "steps", "valid", "jservice-multiple.steps.yml"),
            fail_fast=False
        )
    stdout_no_fail_fast = f.getvalue()

    try:
        verify_api(
            os.path.join(
                "test", "fixtures", "specs", "valid", "jservice_incorrect1.spec.yml"
            ),
            os.path.join("test", "fixtures", "steps", "valid", "jservice-multiple.steps.yml"),
            fail_fast=True
        )
    except ResponseValidationError as e:
        assert stdout_no_fail_fast != str(e)


def test_verbose():
    f = io.StringIO()
    with redirect_stdout(f):
        verify_api(
            os.path.join(
                "test", "fixtures", "specs", "valid", "jservice_incorrect1.spec.yml"
            ),
            os.path.join("test", "fixtures", "steps", "valid", "jservice-multiple.steps.yml"),
            verbose=False
        )
    stdout_no_verbose = f.getvalue()

    f = io.StringIO()
    with redirect_stdout(f):
        verify_api(
            os.path.join(
                "test", "fixtures", "specs", "valid", "jservice_incorrect1.spec.yml"
            ),
            os.path.join("test", "fixtures", "steps", "valid", "jservice-multiple.steps.yml"),
            verbose=True
        )
    stdout_verbose = f.getvalue()

    assert "Traceback (most recent call last):" in stdout_verbose
    assert stdout_no_verbose != stdout_verbose


def test_bandwidth_messaging():
    os.environ["BW_USERNAME"] = ""
    os.environ["BW_PASSWORD"] = ""

    verify_api(
        os.path.join("test", "fixtures", "specs", "valid", "messaging.json"),
        os.path.join("test", "fixtures", "steps", "valid", "messaging.yml"),
        fail_fast=True,
        verbose=True
    )
