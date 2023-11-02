import os
import re

from .errors import (
    InsufficientCoverageError,
    UndocumentedOperationError,
    BaseContextError,
    EvaluationError,
    EnvironmentVariableError,
)
from rich import print


def get_operation_coverage(steps: dict, spec: dict):
    steps_operations = set()
    for operation in steps["steps"]:
        steps_operations.add(operation["operation_id"])

    spec_operations = set()
    for path in spec["paths"]:
        for method in spec["paths"][path]:
            op_id = spec["paths"][path][method]["operationId"]
            spec_operations.add(op_id)

    return steps_operations, spec_operations


def check_operation_coverage(steps: dict, spec: dict):
    steps_operations, spec_operations = get_operation_coverage(steps, spec)

    covered = spec_operations & steps_operations
    uncovered = spec_operations - steps_operations
    undocumented = steps_operations - spec_operations

    proportion_covered = len(covered) / (
        len(covered) + len(uncovered) + len(undocumented)
    )

    if len(undocumented) > 0:
        has_undocumented_operations = True
    else:
        has_undocumented_operations = False

    # If any undocumented operations, immediately halt
    print("--Checking for Uncovered Operations--")
    if has_undocumented_operations:
        raise UndocumentedOperationError(undocumented)

    # Check if operation coverage meets threshold
    print("--Validating Coverage Threshold--")
    if "coverage_threshold" in steps:
        target_coverage: float = steps["coverage_threshold"]

        if proportion_covered < target_coverage:
            raise InsufficientCoverageError(
                proportion_covered, target_coverage, uncovered
            )

    print("[bold green]--Coverage Threshold Met--[/bold green]")


def evaluate(expression: any, steps={}) -> any:
    """
    Recursively evaluate nested expressions using depth-first search.
    Eventually the evaluation result as a string is returned.
    The only allowed base contexts are "env" and "steps".
    Args:
        expression (str): Object of any type that may contain expression(s)
    Raises:
        EnvironmentVariableError:
            if the expression represents an environment variable but it cannot be found
    Returns:
        The evaluated result as a string if there is any expression, original value otherwise.
    """

    if expression is None:
        return

    # Evaluate each value in a dictionary
    if isinstance(expression, dict):
        return dict(map(lambda x: (x[0], evaluate(x[1], steps)), expression.items()))

    # Evaluate each element in a list
    if isinstance(expression, list):
        return list(map(lambda x: evaluate(x, steps), expression))

    if not isinstance(expression, str):
        return expression

    matches: list[str] = re.findall(r"(\${{[^/}]*}})", expression)
    if not matches:
        return expression

    for match in matches:
        value = match.removeprefix("${{").removesuffix("}}").strip()
        base = value.split(".").pop(0)

        if base == "env":
            # Only split at the first dot
            result = os.environ.get(value.split(".", 1)[1])
            if result is None:
                raise EnvironmentVariableError(value)
        elif base == "steps":
            value_array = value.split(".")
            value_dict = f"{value_array[0]}['{value_array[1]}']['{value_array[2]}'].{value_array[3]}"
            for idx, val in enumerate(value_array):
                if idx > 3:
                    value_dict += f"['{val}']"
            try:
                result = eval(value_dict)
            except AttributeError as e:
                raise EvaluationError(e)
        else:
            raise BaseContextError(base)

        # Only replace the first occurrence
        expression = expression.replace(match, str(result), 1)

    return expression
