from .errors import (
    InsufficientCoverageError,
    UndocumentedOperationError,
)

def get_operation_coverage(steps: dict, spec: dict):
    steps_operations = set()
    for operation in steps['steps']:
        steps_operations.add(operation['operation_id'])

    spec_operations = set()
    for path in spec['paths']:
        for method in spec['paths'][path]:
            op_id = spec['paths'][path][method]['operationId']
            spec_operations.add(op_id)
    
    return steps_operations, spec_operations

def check_operation_coverage(steps: dict, spec: dict):
    steps_operations, spec_operations = get_operation_coverage(steps, spec)
    
    covered=spec_operations & steps_operations
    uncovered=spec_operations - steps_operations
    undocumented=steps_operations - spec_operations

    proportion_covered = len(covered) / (len(covered) + len(uncovered) + len(undocumented))
    
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
