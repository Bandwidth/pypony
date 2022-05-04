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
def get_operation_coverage(spec: dict, step: dict) -> EndpointCoverage:
    """
    Given a parsed spec and step file, determine the operations in the spec that are achieved by the step file.

    Args:
        spec (dict): specification file parsed as dict
        step (dict): step file parsed as dict

    Returns:
        OperationCoverage: A dataclass containing the operations covered, uncovered, and undocumented
    """
    print('---Checking Operation Coverage---')

    # Get all operations in the spec file
    spec_operations = set()
    for path in spec['paths']:
        for method in spec['paths'][path]:
            op_id = spec['paths'][path][method]['operationId']
            spec_operations.add(op_id)

    # Get all operations in the step file
    step_operations = set()
    for operation in step['operations']:
        step_operations.add(operation['operation_id'])

    return EndpointCoverage(
        covered=spec_operations & step_operations,
        uncovered=spec_operations - step_operations,
        undocumented=step_operations - spec_operations,
    )
