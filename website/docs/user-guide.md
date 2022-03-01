---
sidebar_position: 2
---

# User Guide

## Installation

```sh
pip install pypony
```

## Arguments

| Argument    | Default | Required | Description | 
|:------------|:--------:|:--------:|:------------|
| `spec_file` | `N/A`    | Yes      | Path to an OpenAPI spec file within your repo. It should either be in JSON or YAML format. | 
| `step_file` | `N/A`    | Yes      | Path to the step file corresponding to your spec_file. See How to Write a Step File for information on the structure of a step file. | 
| `fail_fast` | `false`  | No       | Cancel all subsequent steps running if any step is not valid. | 
| `verbose`   | `false`  | No       | Print the detailed stacktrace if any exception is raised. | 

## Run 

```sh
pypony --spec_file ./specs/my_spec.js --step_file ./steps/my_steps.yml -v -ff
```

## Step Files

Step files describe what requests our action should make. In order to validate your API. They can be written in JSON or YAML. Although you can view our steps file JSON schema for yourself here, and examples of valid specs here, this section will go through the schema with examples and detail how certain features work.

Below is a small example of a steps file for example.com

```yaml
coverage_threshold: 0.8
base_url: https://example.com
paths:
  /person:
    post:
      operationId: createPerson
      steps:
        - name: createPerson
          method: POST
          url: /person
          headers:
            Content-Type: application/json
          body:
            name: John Doe
            age: 42
        - name: getPerson
          method: GET
          url: /person
          params:
            id: ${{ steps.createPerson.response.body.id }}
          auth:
            username: ${{ env.username }}
            password: ${{ env.password }}
```

### Basic Structure

At the top level of a steps file, there are two required fields: `base_url` and `paths`. The `base_url` parameter is the base URL to which all requests will be sent. Paths is an object and is explained below.

The `coverage_threshold` parameter is optional. If present, the action will compare the paths present in the spec to the paths present in the steps. If the proportion of paths present in the steps to paths present in the spec is less than the threshold, the action will fail and report which endpoints are uncovered. No matter if the `coverage_threshold` is present, the action will check for undocumented endpoints: those that are present in the steps but not the spec. If any of these are found, the action will fail.

Warning: The base_url should be a URL without a trailing slash and without query parameters. However, our schema enforces only that it must be a valid URI according to RFC3986.

#### The `paths` Object

The `paths` object contains a collection of path objects. The key for each path object must match the regular expression `^(\/(\w*|[\{\}]))+$`.

Each path object is itself an object that contains a collection of keys. Each of these keys must be one of the following HTTP verbs: `GET`, `PUT`, `POST`, `DELETE`, or `PATCH`. These verbs are case-insensitive.

The value from each HTTP verb key is called a step-list. Each step list must contain the following two keys: `operationId` and `steps`. The `operationId` value can be any string. The `steps` value is an array of `step` objects.


#### The `step` Object

The step object contains the following keys:

* `name` (Required) — This name identifies the step, which is used for referencing previous steps. The value can be any string that matches the regular expression \w+. Within each step list, the value of each name should be unique.
* `method` (Required) — This is the HTTP verb that defines the request type. It can any of `GET`, `PUT`, `POST`, `DELETE`, or `PATCH`. These verbs are case-insensitive.
* `url` (Required) — This is the unique part of the URL to which the request will be sent. You should not include the base URL in this value. You should not include any query parameters. Instead, those should be specified in the params object.
* `headers` — These are the HTTP headers that will be sent with the request.
* `body` — This is is any data that will be sent in the request body.
* `params` — This is any data that will be sent as part of the URL query (i.e. the stuff after ?).
* `auth` — This is an object that contains two keys: `username` and `password`. These values are used in basic HTTP authorization.

### Step References 

#### Referencing Previous Steps

You are able to reference the results of previous steps in the same `step-list`. This allows you to use the results of a previous step in a subsequent one. This can be useful if you don't know the exact value that the target API will return.

To do this, you put the value inside of `${{ ... }}`, similar to how you would reference a secret or environment variable in a GitHub Actions workflow file. Inside these braces, you first say `steps` to signify that you're referencing steps. Next, you give the `name` of a previous step in the same step list, then either `request` to reference the request, or `response` to reference the response to the request. You can then reference various parts of the request or response, like `body` or `headers`. For example, if a previous step's name is `createPerson`, which has the following JSON response:

```json
{
  "id": "12345",
}
```

Then our current step could reference the value of this ID with the following syntax:

```yaml
- name: getPerson
  method: GET
  url: /person
  params:
    id: ${{ steps.createPerson.response.body.id }}
```

If the `base_url` for the steps is `https://example.com`, this would result in a GET request being sent to `https://example.com/person?id=%2212345%22`.

Expressions can also be used in URLs, which will be interpolated one by one and resulted in an evaluated string.

```yaml
- name: getTransactionsOfUser
  method: PUT
  url: /users/${{ steps.createUser.response.body.id }}/transactions/${{ steps.getTransactions.response[0].body.id }}
```

The URL will now become `https://example.com/users/12345/transactions/67890`.

#### Referencing Environment Variables

Using the same `${{ ... }}` syntax as you use to reference previous steps, you can reference environment variables by having the first item within the brackets be `env`. You can then give the name of the environment variable. For example, you can reference the environment variables `username` and `password` with the following syntax:

```yaml
- name: getIndex
  method: GET
  url: /
  auth:
    username: ${{ env.username }}
    password: ${{ env.password }}
```

:::caution Warning
 This package resolves these previous step and environment variable references using the eval function. This means that you may have the ability to do more complex things than simply get a reference. For example, you might reverse a string with `${{ steps.createPerson.response.body.id[::-1] }}`. However, any of these "features" are not officially supported, so we strongly recommend against using them.
:::

:::danger Security Consideration
 This package uses the [eval function](https://docs.python.org/3/library/functions.html#eval) to resolve previous step and environment variable references. This means one might be able to execute arbitrary code inside these references. So, this action should not be run on code you do not trust (e.g. pull requests from outsiders).
:::
