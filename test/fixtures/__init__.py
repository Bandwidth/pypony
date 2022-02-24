"""This module imports all the fixtures."""

import glob
import os

import pytest


def use_fixture(*path):
    """Helper method for getting all files in a directory"""

    return sorted(
        glob.glob(os.path.join("test", "fixtures", *path)),
        key=os.path.basename,
    )


@pytest.fixture
def valid_specs():
    return use_fixture("specs", "valid", "*")


@pytest.fixture
def invalid_specs():
    return use_fixture("specs", "invalid", "*")


@pytest.fixture
def valid_steps():
    return use_fixture("steps", "valid", "*")


@pytest.fixture
def invalid_steps():
    return use_fixture("steps", "invalid", "*")


@pytest.fixture
def invalid_scanner_steps():
    return use_fixture("steps", "invalid", "scanner", "*")


@pytest.fixture
def invalid_schema_steps():
    return use_fixture("steps", "invalid", "schema", "*")
