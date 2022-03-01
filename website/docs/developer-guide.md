---
sidebar_position: 3
---

# Developer Guide

## Run Tests 

Run the following command from the root directory of the project:

```sh
coverage run -m pytest -vv
```

You should see some output listing every unit test and indicating that it passed. If you see that every unit test passed, you can run the following command to see a coverage report that lists which lines in each source file are not covered.

```sh
coverage report -m
```
