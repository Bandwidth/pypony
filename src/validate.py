from .parsing import parse_steps_file, parse_spec_file
from .preprocessing import check_operation_coverage
from .requests import make_requests
# from .verify import verify_request

def validate(step_file_path: str, spec_file_path: str, fail_fast: bool = False, verbose: bool = False):
    
    # convert step and spec into usable dictionaries
    print("--Validating Steps--")
    steps = parse_steps_file(step_file_path)
    
    print("--Validating Spec--")
    spec, operation_schemas = parse_spec_file(spec_file_path)

    # Validate that desired coverage threshold is met (if present)
    check_operation_coverage(steps, spec)

    print("--Making Requests--")
    make_requests(steps, operation_schemas, fail_fast, verbose)


