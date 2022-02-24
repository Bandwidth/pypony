# -*- coding: utf-8 -*-
"""context.py

Context manages all variables used during validation,
like system environment variables and responses of previous steps.
"""

import os
import re
from types import SimpleNamespace

from .singleton import Singleton
from .errors import BaseContextError, EvaluationError, EnvironmentVariableError


class Context(metaclass=Singleton):
    """
    The global context object will be used as a singleton across the entire system.
    """

    _steps = SimpleNamespace()

    @property
    def steps(self):
        return self._steps

    def add_steps(self, step):
        """
        Adds a Step object as an attribute of `self.steps`

        Args:
            step (Step): the Step object to add
        """

        setattr(self.steps, step.name, step)

    def clear_steps(self):
        """
        Clears all Steps objects from attributes of `self.steps`
        """

        self._steps = SimpleNamespace()

    # noinspection PyMethodMayBeStatic
    def evaluate(self, expression: any) -> any:
        """
        Recursively evaluate nested expressions using depth-first search.
        Eventually the evaluation result as a string is returned.

        The only allowed base contexts are "env" and "steps".

        Args:
            expression (str): Object of any type that may contain expression(s)

        Raises:
            EnvironmentVariableError:
                if the expression represents an environment variable but it cannot be found

        Returns:
            The evaluated result as a string if there is any expression, original value otherwise.
        """

        if expression is None:
            return

        # Evaluate each value in a dictionary
        if isinstance(expression, dict):
            return dict(map(lambda x: (x[0], self.evaluate(x[1])), expression.items()))

        # Evaluate each element in a list
        if isinstance(expression, list):
            return list(map(lambda x: self.evaluate(x), expression))

        if not isinstance(expression, str):
            return expression

        matches: list[str] = re.findall(r"(\${{[^/}]*}})", expression)
        if not matches:
            return expression

        for match in matches:
            value = match.removeprefix("${{").removesuffix("}}").strip()
            base = value.split(".").pop(0)

            if base == "env":
                # Only split at the first dot
                result = os.environ.get(value.split(".", 1)[1])
                if result is None:
                    raise EnvironmentVariableError(value)
            elif base == "steps":
                try:
                    result = eval("self." + value)
                except AttributeError as e:
                    raise EvaluationError(e)
            else:
                raise BaseContextError(base)

            # Only replace the first occurrence
            expression = expression.replace(match, str(result), 1)

        return expression
