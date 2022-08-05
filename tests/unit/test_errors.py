import pytest

from src.errors import *

operation_set: set[str] = {"op_one", "op_two", "op_three"}


def test_undocumented_operation_error():
    with pytest.raises(UndocumentedOperationError) as err:
        raise UndocumentedOperationError(operation_set)


def test_insufficient_coverage_error():
    with pytest.raises(InsufficientCoverageError) as err:
        raise InsufficientCoverageError(90.0, 100.0, operation_set)


def test_invalid_file_error():
    with pytest.raises(InvalidFileError) as err:
        raise InvalidFileError(extension=".json")


def test_base_context_error():
    with pytest.raises(BaseContextError) as err:
        raise BaseContextError(value="not env or steps")


def test_evaluation_error():
    with pytest.raises(EvaluationError) as err:
        raise EvaluationError(message="evaluation error")


def test_environment_variable_error():
    with pytest.raises(EnvironmentVariableError) as err:
        raise EnvironmentVariableError(value="NON_EXISTENT_ENV")


def test_invalid_expression_error():
    with pytest.raises(InvalidExpressionError) as err:
        raise InvalidExpressionError(value="2 + 2 = fish")


def test_unsupported_schema_error():
    with pytest.raises(UnsupportedSchemaError) as err:
        raise UnsupportedSchemaError(value="application/xml")
