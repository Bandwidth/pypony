# PyPony

[![Unit Tests](https://github.com/Bandwidth/pypony/actions/workflows/ci.yml/badge.svg)](https://github.com/Bandwidth/pypony/actions/workflows/ci.yml)

PyPony is a Python CLI tool for contract testing OpenAPI specifications against the live APIs that they define.  

## Documentation

- [Source Code Docs](https://fuzzy-journey-0f130eaf.pages.github.io/)
- [User's Guide](https://fuzzy-journey-0f130eaf.pages.github.io/docs/users-guide/)
- [Developer's Guide](https://fuzzy-journey-0f130eaf.pages.github.io/docs/developers-guide/)

## Sample Steps File

```yml
coverage_threshold: 0.0
base_url: http://127.0.0.1:8000
steps:
  - name: coveredOperation
    operation_id: coveredOperation
    method: GET
    url: /
    status_code: 200
```
