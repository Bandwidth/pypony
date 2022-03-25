# -*- coding: utf-8 -*-
"""preprocessing.py

This module contains functions to ensure compatibility for a step file and corresponding spec file.
It will check that every method referenced in the step file exists in the spec file.
"""
from rich import print, inspect
from dataclasses import dataclass

# TODO: refactor to `OperationCoverage`
@dataclass
class EndpointCoverage:
    """
    Dictionary classifying endpoints into three categories:
        - covered: endpoints that are called in the step file and documented in the spec file
        - uncovered: endpoints that are in the spec file but not called in the step file
        - undocumented: endpoints that are called in the step file but not documented in the spec file
    """

    covered: set[str]
    uncovered: set[str]
    undocumented: set[str]

    def has_undocumented_endpoints(self) -> bool:
        return len(self.undocumented) > 0

    def proportion_covered(self) -> float:
        return len(self.covered) / (
            len(self.covered) + len(self.uncovered) + len(self.undocumented)
        )


# TODO: refactor to `get_operation_coverage`
def get_endpoint_coverage(spec: dict, step: dict) -> EndpointCoverage:
    """
    Given a parsed spec and step file, determine the endpoints in the spec that are achieved by the step file.

    Args:
        spec (dict): specification file parsed as dict
        step (dict): step file parsed as dict

    Returns:
        EndpointCoverage: A dataclass containing the endpoints covered, uncovered, and undocumented
    """
    print('---Checking Operation Coverage---')

    # TODO: Instead of getting the `paths` make a list of all of the operations in the spec and step files and compare them
    # Get all endpoints in the spec file
    spec_endpoints = set(spec["paths"].keys())

    # Get all endpoints in the step file
    step_endpoints = set(step["paths"].keys())

    return EndpointCoverage(
        covered=spec_endpoints & step_endpoints,
        uncovered=spec_endpoints - step_endpoints,
        undocumented=step_endpoints - spec_endpoints,
    )
