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


from typing import Optional
from pydantic import BaseModel, Field
from Pieces._pieces_lib.pieces_os_client.models.classification import Classification
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class TrackedAssetEventFormatReclassificationMetadata(BaseModel):
    """
    Metadata of a format reclassification event  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    previous: Optional[Classification] = None
    current: Optional[Classification] = None
    __properties = ["schema", "previous", "current"]

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
    def from_json(cls, json_str: str) -> TrackedAssetEventFormatReclassificationMetadata:
        """Create an instance of TrackedAssetEventFormatReclassificationMetadata from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of previous
        if self.previous:
            _dict['previous'] = self.previous.to_dict()
        # override the default output from pydantic by calling `to_dict()` of current
        if self.current:
            _dict['current'] = self.current.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TrackedAssetEventFormatReclassificationMetadata:
        """Create an instance of TrackedAssetEventFormatReclassificationMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TrackedAssetEventFormatReclassificationMetadata.parse_obj(obj)

        _obj = TrackedAssetEventFormatReclassificationMetadata.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "previous": Classification.from_dict(obj.get("previous")) if obj.get("previous") is not None else None,
            "current": Classification.from_dict(obj.get("current")) if obj.get("current") is not None else None
        })
        return _obj


