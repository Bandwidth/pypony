from .models import Step
from .verify import verify

from rich import print, print_json, inspect

def make_requests(steps: dict, spec: dict, fail_fast: bool, verbose: bool):

    base_url: str = steps["base_url"]

    # Set global auth if it exists in the step file
    global_auth: dict = {}
    if 'auth' in steps.keys():
        global_auth: dict = steps["auth"]
    
    # Get steps list
    steps: list = steps["steps"]

    # Create responses dict for easier parsing
    operation_responses: dict = {}
    for path in spec['paths']:
        for method in spec['paths'][path]:
            op_id = spec['paths'][path][method]['operationId']
            operation_responses[op_id] = spec['paths'][path][method]['responses']

    for s in steps:
        step = Step(s)
        request = step.construct_request(base_url)
        # response = request.send_request()
