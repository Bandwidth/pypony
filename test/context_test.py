import os
import uuid

import pytest

from src.models import Context, Step, Request
from src.models.errors import BaseContextError, EnvironmentVariableError


@pytest.fixture
def context():
    return Context()


@pytest.fixture(autouse=True)
def cleanup(context):
    context.clear_steps()
    yield
    context.clear_steps()


def _env(value):
    return "${{ env." + value + " }}"


def _steps(value):
    return "${{ steps." + value + " }}"


def test_step_add(context):
    step = Step(
        name="createUser",
        request=Request(
            operation_id="createUser", 
            method="POST", 
            url="http://localhost:8000/users",
            status_code=200
        )
    )
    context.add_steps(step)

    assert context.steps.createUser == step


def test_step_add_duplicated(context):
    for i in range(5):
        context.add_steps(
            Step(
                name="createUser",
                request=Request(
                    operation_id="createUser",
                    method="POST", 
                    url="http://localhost:8000/users",
                    status_code=200
                )
            )
        )

    assert len(vars(context.steps)) == 1


def test_step_clear(context):
    context.add_steps(
        Step(
            name="createUser",
            request=Request(
                operation_id="createUser",
                method="POST", 
                url="http://localhost:8000/users",
                status_code=200
            )
        )
    )
    context.add_steps(
        Step(
            name="getUsers",
            request=Request(
                operation_id="getUsers",
                method="GET", 
                url="http://localhost:8000/users",
                status_code=200
            )
        )
    )
    assert len(vars(context.steps)) == 2

    context.clear_steps()
    assert len(vars(context.steps)) == 0


# Expression.evaluate() delegates Context.evaluate()
def test_evaluate_single(context):
    key = "USER_UUID"
    val = str(uuid.uuid4())
    os.environ[key] = val

    assert context.evaluate(_env(key)) == val


def test_evaluate_single_with_dots(context):
    key = "USER.UUID.TOKEN"
    val = str(uuid.uuid4())
    os.environ[key] = val

    assert context.evaluate(_env(key)) == val

    os.environ.pop(key)


def test_evaluate_multiple(context):
    key1 = "USER.UUID.TOKEN1"
    val1 = str(uuid.uuid4())
    os.environ[key1] = val1

    key2 = "USER.UUID.TOKEN2"
    val2 = str(uuid.uuid4())
    os.environ[key2] = val2

    assert context.evaluate(_env(key1) + _env(key2)) == val1 + val2


def test_evaluate_url(context):
    user_id = str(uuid.uuid4())
    account_id = str(uuid.uuid4())
    context.add_steps(
        Step(
            name="createUser", 
            request=Request(
                operation_id="createUser",
                body={"id": user_id}, url="", 
                method="",
                status_code=200
            )
        )
    )
    context.add_steps(
        Step(
            name="createAccount",
            request=Request(
                operation_id="createAccount",
                body={"id": account_id}, 
                url="", 
                method="",
                status_code=200
            )   
        )
    )

    assert (
        context.evaluate(
            f"/users/{_steps('createUser.request.body.id')}/accounts/{_steps('createAccount.request.body.id')}"
        )
        == f"/users/{user_id}/accounts/{account_id}"
    )


def test_evaluate_environment_variable_not_found_error(context):
    key = "USER.UUID"
    os.environ.pop(key, None)
    assert key not in os.environ

    with pytest.raises(EnvironmentVariableError):
        context.evaluate(_env(key))


def test_evaluate_base_context_error(context):
    with pytest.raises(BaseContextError):
        context.evaluate("${{ hello.world }}")
