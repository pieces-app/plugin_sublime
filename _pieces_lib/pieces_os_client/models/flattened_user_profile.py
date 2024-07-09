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

class FlattenedUserProfile(BaseModel):
    """
    This is a FlattenedUserProfile that includes information that is not sensative in relation to a user.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    id: StrictStr = Field(default=..., description="this is the uuid that identifies a user.")
    email: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    username: Optional[StrictStr] = None
    picture: Optional[StrictStr] = None
    vanityname: Optional[StrictStr] = None
    __properties = ["schema", "id", "email", "name", "username", "picture", "vanityname"]

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
    def from_json(cls, json_str: str) -> FlattenedUserProfile:
        """Create an instance of FlattenedUserProfile from a JSON string"""
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
    def from_dict(cls, obj: dict) -> FlattenedUserProfile:
        """Create an instance of FlattenedUserProfile from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FlattenedUserProfile.parse_obj(obj)

        _obj = FlattenedUserProfile.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "id": obj.get("id"),
            "email": obj.get("email"),
            "name": obj.get("name"),
            "username": obj.get("username"),
            "picture": obj.get("picture"),
            "vanityname": obj.get("vanityname")
        })
        return _obj


