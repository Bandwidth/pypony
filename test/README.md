# Testing

`test` folder contains all test files for this project.

## Folder Structure

- `/test`
  - `validate_test.py`
  - `...`
  - `/fixtures` (mock data)
    - `/specs`
      - `test_spec.yaml`
      - `...`
    - `/steps`
      - `test_steps.yaml`
      - `...`
    - `/...`

## Get Started

### Create Tests

All test files and functions should either start with `test_` or end with `_test`. For example:

- `test_example.py`
- `example_test.py`

### Use Fixtures

```python
# example_test.py

import os

test_spec = os.path.join('fixtures', 'specs', 'test_spec.yml')
```

It is recommended to create fixtures using the pytest fixture decorator `@pytest.fixture`:

```python
# example_test.py

import os
import pytest


@pytest.fixture
def test_spec_file(): return os.path.join('fixtures', 'specs', 'test_spec.yml')


def test_parse_spec(test_spec_file):  # Add fixture names as parameters here
  # Access fixtures without parentheses
  assert test_spec_file != ''
```

Access fixtures with parentheses, otherwise

```python
# example_test.py

import os
import pytest


@pytest.fixture
def test_spec_file(): return os.path.join('fixtures', 'specs', 'test_spec.yml')


def test_parse_spec():
  # Access fixtures without parentheses
  assert test_spec_file() != ''
```

would result in:

```
action_test.py::test_parse_spec FAILED                                   [ 33%]
action_test.py:16 (test_parse_spec)
Fixture "test_spec_file" called directly. Fixtures are not meant to be called directly,
but are created automatically when test functions request them as parameters.
See https://docs.pytest.org/en/stable/fixture.html for more information about fixtures, and
https://docs.pytest.org/en/stable/deprecations.html#calling-fixtures-directly about how to update your code.
```

### Run Tests

See https://docs.pytest.org/en/6.2.x/pythonpath.html

> Running pytest with `pytest [...]` instead of `python -m pytest [...]` yields nearly equivalent behaviour, except that the latter will add the current directory to `sys.path`, which is standard `python` behavior.

To run all test suites:

```shell
python3 -m pytest
```

To run a single or multiple test suites:

```shell
python3 -m pytest -k <file1> <file2> ...
```

### Coverage

Code coverage is measured using `coverage` library.

```
coverage run -m pytest
```

To report results in terminal:

```
coverage report -m
```

To report results in HTML:

```
coverage html
```

Open `htmlcov/index.html` in your browser to see the report
