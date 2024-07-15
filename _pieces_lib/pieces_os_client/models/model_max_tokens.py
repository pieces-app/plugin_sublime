# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional, Union
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictFloat, StrictInt
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class ModelMaxTokens(BaseModel):
    """
    This will describe the MaxTokens for an MLModel  total is required.  iff there is a differentiator with inputs/outputs, then we can also provide those as well.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    total: Optional[Union[StrictFloat, StrictInt]] = Field(...)
    input: Optional[Union[StrictFloat, StrictInt]] = None
    output: Optional[Union[StrictFloat, StrictInt]] = None
    __properties = ["schema", "total", "input", "output"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> ModelMaxTokens:
        """Create an instance of ModelMaxTokens from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of var_schema
        if self.var_schema:
            _dict['schema'] = self.var_schema.to_dict()
        # set to None if total (nullable) is None
        # and __fields_set__ contains the field
        if self.total is None and "total" in self.__fields_set__:
            _dict['total'] = None

        # set to None if input (nullable) is None
        # and __fields_set__ contains the field
        if self.input is None and "input" in self.__fields_set__:
            _dict['input'] = None

        # set to None if output (nullable) is None
        # and __fields_set__ contains the field
        if self.output is None and "output" in self.__fields_set__:
            _dict['output'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ModelMaxTokens:
        """Create an instance of ModelMaxTokens from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ModelMaxTokens.parse_obj(obj)

        _obj = ModelMaxTokens.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "total": obj.get("total"),
            "input": obj.get("input"),
            "output": obj.get("output")
        })
        return _obj


