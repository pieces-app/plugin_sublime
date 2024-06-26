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
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.flattened_user_profile import FlattenedUserProfile

class SeededAccessor(BaseModel):
    """
    This is a pre-created accessor that simply takes an os id and an optional user(flattened)  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(None, alias="schema")
    os: StrictStr = Field(..., description="this is an os id.")
    user: Optional[FlattenedUserProfile] = None
    share: StrictStr = Field(..., description="this is the share that the asset is apart of.")
    __properties = ["schema", "os", "user", "share"]

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
    def from_json(cls, json_str: str) -> SeededAccessor:
        """Create an instance of SeededAccessor from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of user
        if self.user:
            _dict['user'] = self.user.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededAccessor:
        """Create an instance of SeededAccessor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededAccessor.parse_obj(obj)

        _obj = SeededAccessor.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "os": obj.get("os"),
            "user": FlattenedUserProfile.from_dict(obj.get("user")) if obj.get("user") is not None else None,
            "share": obj.get("share")
        })
        return _obj


