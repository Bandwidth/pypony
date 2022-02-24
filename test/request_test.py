from api_validator.models import Request, Context, Step

context = Context()


def test_evaluate_all():
    step = Step(
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
            }
        )
    )

    context.add_steps(step)

    request = Request(
        method='GET',
        url='${{ steps.createUser.request.url }}',
        params={
            'user': {
                'token': '${{ steps.createUser.request.params.token }}'
            }
        },
        body={
            'name': [
                '${{ steps.createUser.request.body.user.name }}',
                '${{ steps.createUser.request.body.user.name }}'
            ]
        }
    )

    request.evaluate_all()

    assert request.url == step.request.url

    # nested dict
    assert request.params.user.token == step.request.params.token

    # list
    for name in request.body.name:
        assert name == step.request.body.user.name
