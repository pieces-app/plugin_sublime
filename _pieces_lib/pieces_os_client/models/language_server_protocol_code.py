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


from typing import Dict, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class LanguageServerProtocolCode(BaseModel):
    """
    NOTE: this can me a union type here.. (integer | string;) so we need to get a bit creative  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    code_integer: Optional[StrictInt] = None
    code_string: Optional[StrictStr] = None
    raw_json: Optional[Dict[str, StrictStr]] = Field(default=None, description="This is a Map<String, String>, basically just a json object for additional data if int/string will not work")
    __properties = ["schema", "code_integer", "code_string", "raw_json"]

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
    def from_json(cls, json_str: str) -> LanguageServerProtocolCode:
        """Create an instance of LanguageServerProtocolCode from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LanguageServerProtocolCode:
        """Create an instance of LanguageServerProtocolCode from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LanguageServerProtocolCode.parse_obj(obj)

        _obj = LanguageServerProtocolCode.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "code_integer": obj.get("code_integer"),
            "code_string": obj.get("code_string"),
            "raw_json": obj.get("raw_json")
        })
        return _obj


