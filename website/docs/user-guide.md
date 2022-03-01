---
sidebar_position: 2
---

# User Guide

## Installation

```sh
pip install pypony
```

## Arguments

Below is a description of the arguments. Arguments are optional unless specified otherwise.

| Argument    | Default | Required | Description | 
|:------------|:--------:|:--------:|:------------|
| `spec_file` | `N/A`    | Yes      | Path to an OpenAPI spec file within your repo. It should either be in JSON or YAML format. | 
| `step_file` | `N/A`    | Yes      | Path to the step file corresponding to your spec_file. See How to Write a Step File for information on the structure of a step file. | 
| `fail_fast` | `false`  | No       | Cancel all subsequent steps running if any step is not valid. | 
| `verbose`   | `false`  | No       | Print the detailed stacktrace if any exception is raised. | 

## Run 

```sh
pypony 
```
