import os
import json

import yaml
from jsonschema import validate, ValidationError
from rich import print, inspect

from .errors import InvalidFileError

def parse_steps_file(step_file_path: str) -> dict:
    try:
        steps_schema_path = os.path.join(os.path.dirname(__file__), "steps_schema.yml")
        with open(steps_schema_path, "r") as step_schema_file:
            steps_schema = yaml.safe_load(step_schema_file.read())
    except FileNotFoundError as e:
        raise FileNotFoundError("Steps schema file not found") from e
    
    try: 
        with open(step_file_path, "r") as step_file:
            steps = yaml.safe_load(step_file.read())
            validate(instance=steps, schema=steps_schema)
    
    except ValidationError as e:
        raise ValidationError(f"Steps file has the following syntax errors: {e.message} ") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Steps file {step_file_path} not found") from e
   
    print("[bold green]--Succesfully Validated Steps File--[/bold green]")
    return steps

def parse_spec_file(spec_file_path: str) -> dict:
    try:
        open_api_schema_path = os.path.join(os.path.dirname(__file__), "open_api_schema.yml")
        with open(open_api_schema_path, "r") as open_api_schema_file:
            open_api_schema = yaml.safe_load(open_api_schema_file.read())
    except FileNotFoundError as e:
        raise FileNotFoundError("API Spec schema file not found") from e
    
    try: 
        with open(spec_file_path, "r") as open_api_file:
            if spec_file_path.lower().endswith('.json'): 
                spec = json.loads(open_api_file.read())
            elif spec_file_path.lower().endswith('.yml') or spec_file_path.lower().endswith('.yaml'):
                spec = yaml.safe_load(open_api_file.read())
            else: 
                raise InvalidFileError(extension=os.path.splitext(spec_file_path)[1])

            # TODO: Resolve all $refs 
            
            validate(instance=spec, schema=open_api_schema)
    
    except ValidationError as e:
        raise ValidationError(f"API Spec file has the following syntax errors: {e.message} ") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"API Spec file {spec_file_path} not found") from e
    
    print("[bold green]--Succesfully Validated Spec File--[/bold green]")
    return spec
