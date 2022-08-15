import pytest

from src.errors import *

# Test Values
operation_set: set[str] = {"op_one", "op_two", "op_three"}
coverage = 90.0
desired_coverage = 100.0
file_extension = ".json"
base_context_value = "not env or steps"
evaluation_error_message = "evaluation error"
environment_variable_value = "NON_EXISTENT_ENV"
expression_value = "2 + 2 = fish"
schema_value = "application/xml"


def test_undocumented_operation_error():
    with pytest.raises(UndocumentedOperationError) as err:
        raise UndocumentedOperationError(operation_set)


def test_insufficient_coverage_error():
    with pytest.raises(InsufficientCoverageError) as err:
        raise InsufficientCoverageError(coverage, desired_coverage, operation_set)


def test_invalid_file_error():
    with pytest.raises(InvalidFileError) as err:
        raise InvalidFileError(file_extension)


def test_base_context_error():
    with pytest.raises(BaseContextError) as err:
        raise BaseContextError(base_context_value)


def test_evaluation_error():
    with pytest.raises(EvaluationError) as err:
        raise EvaluationError(evaluation_error_message)


def test_environment_variable_error():
    with pytest.raises(EnvironmentVariableError) as err:
        raise EnvironmentVariableError(environment_variable_value)


def test_invalid_expression_error():
    with pytest.raises(InvalidExpressionError) as err:
        raise InvalidExpressionError(expression_value)


def test_unsupported_schema_error():
    with pytest.raises(UnsupportedSchemaError) as err:
        raise UnsupportedSchemaError(schema_value)
