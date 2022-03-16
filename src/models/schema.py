# -*- coding: utf-8 -*-
"""schema.py

JSON Schema is a vocabulary that allows you to annotate and validate JSON documents.
"""

from jschon import JSONSchema, JSON
from jschon.jsonschema import Scope

META_SCHEMA = "https://json-schema.org/draft/2020-12/schema"


class Schema:
    """
    Predefines meta schema and stores JSON schema document model.
    """

    def __init__(self, schema: dict, meta_schema: str = META_SCHEMA):
        schema["$schema"] = meta_schema
        self.schema = JSONSchema(schema)

    def evaluate(self, json: dict) -> Scope:
        """
        Verify the JSON against the schema.

        Args:
            json (dict): the JSON document to evaluate

        Returns:
            Evaluate a JSON document and return the complete evaluation result tree.
        """

        return self.schema.evaluate(JSON(json))
