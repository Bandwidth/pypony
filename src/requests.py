from .preprocessing import evaluate
from .models import Step
# from .verify import verify

from rich import print, print_json, inspect

def make_requests(steps: dict, spec: dict, fail_fast: bool, verbose: bool):

    base_url: str = steps["base_url"]

    # Set global auth if it exists in the step file
    global_auth: dict = None
    if 'auth' in steps.keys():
        global_auth: dict = {}
        for key in steps["auth"]:
            print(key)
            # global_auth.update({"ligma", "1"})
    else:
        global_auth = None
    
    # Get steps list
    steps: list = steps["steps"]

    # Create responses dict for easier parsing
    operation_responses: dict = {}
    for path in spec['paths']:
        for method in spec['paths'][path]:
            op_id = spec['paths'][path][method]['operationId']
            operation_responses[op_id] = spec['paths'][path][method]['responses']
    inspect(operation_responses)

    for s in steps:
        step = Step(s)
        request = step.construct_request(base_url, global_auth)
        # inspect(request)
        # response = request.send()
