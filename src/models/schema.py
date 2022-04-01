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
    See https://jschon.readthedocs.io/en/latest/reference/jsonschema.html#jschon.jsonschema.JSONSchema
    See https://jschon.readthedocs.io/en/latest/examples/recursive_schema_extension.html for example
    """

    def __init__(self, schema: dict, meta_schema: str = META_SCHEMA):
        json = {"$schema": meta_schema}

        # TODO: support more content types
        try:
            json.update(schema['content']['application/json']['schema'])
        except KeyError as e:
            print(e)
            print('Key not found. Most likely content type of the response is not supported')

        self.schema = JSONSchema(json)

    def evaluate(self, json: dict) -> Scope:
        """
        Verify the JSON against the schema.

        Args:
            json (dict): the JSON document to evaluate

        Returns:
            Evaluate a JSON document and return the complete evaluation result tree.
        """
        # inspect(self.schema, methods=True)
        return self.schema.evaluate(JSON(json))
