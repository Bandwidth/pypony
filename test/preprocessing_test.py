"""This module contains tests for src/preprocessing.py.
"""

import os
from src.parsing import parse_spec, parse_steps
from src.preprocessing import get_operation_coverage


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
    operation_coverage = get_operation_coverage(spec, step)
    assert not operation_coverage.has_undocumented_operations()


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
    operation_coverage = get_operation_coverage(spec, step)
    assert operation_coverage.has_undocumented_operations()
    assert "/" not in operation_coverage.undocumented


def test_measure_operation_coverage():
    """
    Verify that operation coverage between specs and steps is measured correctly
    """

    step = parse_steps("./test/fixtures/steps/valid/coverage_steps.yml")
    assert "coverage_threshold" in step

    spec = parse_spec("./test/fixtures/specs/valid/coverage_spec.yml")
    operation_coverage = get_operation_coverage(spec, step)

    assert operation_coverage.has_undocumented_operations()
    assert len(operation_coverage.undocumented) == 1
    assert operation_coverage.undocumented == {"undocumentedOperation"}

    assert len(operation_coverage.covered) == 4
    assert operation_coverage.covered == {
        "coveredOperation",
        "postOperation",
        "putOperation",
        "deleteOperation",
    }

    assert len(operation_coverage.uncovered) == 1
    assert operation_coverage.uncovered == {"uncoveredOperation"}

    assert operation_coverage.proportion_covered() == 4 / (1 + 4 + 1)
