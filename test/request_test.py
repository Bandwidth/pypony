from src.models import Request, Context, Operation

context = Context()


def test_evaluate_all():
    operation = Operation(
        'createUser',
        request=Request(
            method='POST',
            url='localhost:8000/users',
            params={'token': '123-abc'},
            body={
                'user':
                    {
                        'name': 'Hello'
                    }
            },
            operation_id='CreateUser',
            status_code=200
        )
    )

    context.add_operations(operation)

    request = Request(
        method='GET',
        url='${{ operations.createUser.request.url }}',
        params={
            'user': {
                'token': '${{ operations.createUser.request.params.token }}'
            }
        },
        body={
            'name': [
                '${{ operations.createUser.request.body.user.name }}',
                '${{ operations.createUser.request.body.user.name }}'
            ]
        },
        operation_id='GetUser',
        status_code=200
    )

    request.evaluate_all()

    assert request.url == operation.request.url

    # nested dict
    assert request.params.user.token == operation.request.params.token

    # list
    for name in request.body.name:
        assert name == operation.request.body.user.name
