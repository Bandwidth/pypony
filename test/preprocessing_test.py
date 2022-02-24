"""This module contains tests for src/preprocessing.py.
"""

import os
from api_validator.parsing import parse_spec, parse_steps
from api_validator.preprocessing import get_endpoint_coverage


def test_compatible_spec_step():
    """
    Tests error handling against a valid spec and step file. All methods referenced in the step exist in the spec.
    """

    step = parse_steps(
        os.path.join(
            "test", "fixtures", "steps", "valid", "localhost_uncovered.step.yml"
        )
    )
    spec = parse_spec(
        os.path.join("test", "fixtures", "specs", "valid", "localhost.spec.yml")
    )
    endpoint_coverage = get_endpoint_coverage(spec, step)
    assert not endpoint_coverage.has_undocumented_endpoints()


def test_missing_spec_method():
    """
    Verify error handling function can identify missing method in spec file that is referenced in step file.
    """

    spec = parse_spec(
        os.path.join(
            "test", "fixtures", "specs", "valid", "localhost_undocumented.spec.yml"
        )
    )
    step = parse_steps(
        os.path.join("test", "fixtures", "steps", "valid", "localhost.step.yml")
    )
    endpoint_coverage = get_endpoint_coverage(spec, step)
    assert endpoint_coverage.has_undocumented_endpoints()
    assert "/" not in endpoint_coverage.undocumented


def test_measure_endpoint_coverage():
    """
    Verify that endpoint coverage between specs and steps is measured correctly
    """

    step = parse_steps("./test/fixtures/steps/valid/coverage_steps.yml")
    assert "coverage_threshold" in step

    spec = parse_spec("./test/fixtures/specs/valid/coverage_spec.yml")
    endpoint_coverage = get_endpoint_coverage(spec, step)

    assert endpoint_coverage.has_undocumented_endpoints()
    assert len(endpoint_coverage.undocumented) == 1
    assert endpoint_coverage.undocumented == {"/undocumented_path"}

    assert len(endpoint_coverage.covered) == 4
    assert endpoint_coverage.covered == {
        "/covered_path",
        "/nested/path",
        "/doubly/nested/path",
        "/path/{with}/braces",
    }

    assert len(endpoint_coverage.uncovered) == 1
    assert endpoint_coverage.uncovered == {"/uncovered_path"}

    assert endpoint_coverage.proportion_covered() == 4 / (1 + 4 + 1)
