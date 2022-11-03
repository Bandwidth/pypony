# PyPony

[![Unit Tests](https://github.com/Bandwidth/pypony/actions/workflows/ci.yml/badge.svg)](https://github.com/Bandwidth/pypony/actions/workflows/ci.yml)

PyPony is a 🪄magical🪄 Python CLI tool for contract testing OpenAPI specifications against the live APIs that they define.

## Supported OAS Features

* JSON or YAML
* enums
* $ref
* oneOf

## Install Locally

```sh
cd pypony
pip install .
```

## Run

```sh
pypony -st ./my_steps.yml -sp ./my_spec.yml  -v
```

### Arguments

| Argument             | Description |
|:--------------------:|:------------|
| '-st', '--step'      | Relative path to step file |
| '-sp', '--spec'      | Relative path to spec file |
| '-v', '--verbpse'    | Boolean verbose output (default=`False`) |
| '-ff', '--fail-fast' | Option to fail fast if an exception is encountered (default=`False`) | # Coming soon!

## Step File

The `step` file is what is used to make API calls - its where you provide information like base url, auth, path, request body, etc. PyPony uses the information in the step file to check against the OpenAPI spec, ensuring it matches the definiution, and then sends it using the [requests](https://pypi.org/project/requests/) library.

Step files export expressions and environment variables, allowing it to be run in a CI/CD pipeline and making data from previous steps accessible.

### Required Step File Fields

* BaseURL
* Steps
  * name
  * operation_id
  * method
  * path
  * status_code

### Example Step File

```yml
---
base_url: https://voice.bandwidth.com/api/v2
auth:
    username: ${{ env.BW_USERNAME }}
    password: ${{ env.BW_PASSWORD }}
steps:
  - name: createCall
    operation_id: createCall
    method: POST
    path: /accounts/${{ env.BW_ACCOUNT_ID }}/calls
    headers:
      Content-Type: application/json
    body:
      to: ${{ env.USER_NUMBER }}
      from: ${{ env.BW_NUMBER }}
      applicationId: ${{ env.BW_VOICE_APPLICATION_ID }}
      answerUrl: ${{ env.BW_ANSWER_URL }}
    status_code: 201

  - name: Get Call Info
    operation_id: getCallState
    method: GET
    path: /accounts/${{ env.BW_ACCOUNT_ID }}/calls/${{ steps.createCall.response.data.callId }}
    auth:    # overrides global auth definition
        username: ${{ env.VOXBONE_USERNAME }}
        password: ${{ env.VOXBONE_PASSWORD }}
    status_code: 200

  - name: listConferences
    operation_id: listConferences
    method: GET
    path: /accounts/${{ env.BW_ACCOUNT_ID }}/conferences
    status_code: 200
```

The full step file schema can be found [here](https://github.com/Bandwidth/pypony/blob/main/src/steps_schema.yml).
