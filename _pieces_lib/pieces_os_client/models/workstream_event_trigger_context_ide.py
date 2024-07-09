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
from pydantic import BaseModel, Field, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class WorkstreamEventTriggerContextIDE(BaseModel):
    """
    This is the given context for an IDE.  tabs: this here refers to the tabs w/in the IDE.  Modules here are the given repositories  Name: this is the name of a workspace, but not required.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    tabs: Optional[IDETabs] = None
    modules: Optional[ProjectModules] = None
    name: Optional[StrictStr] = None
    __properties = ["schema", "tabs", "modules", "name"]

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
    def from_json(cls, json_str: str) -> WorkstreamEventTriggerContextIDE:
        """Create an instance of WorkstreamEventTriggerContextIDE from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of tabs
        if self.tabs:
            _dict['tabs'] = self.tabs.to_dict()
        # override the default output from pydantic by calling `to_dict()` of modules
        if self.modules:
            _dict['modules'] = self.modules.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WorkstreamEventTriggerContextIDE:
        """Create an instance of WorkstreamEventTriggerContextIDE from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WorkstreamEventTriggerContextIDE.parse_obj(obj)

        _obj = WorkstreamEventTriggerContextIDE.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "tabs": IDETabs.from_dict(obj.get("tabs")) if obj.get("tabs") is not None else None,
            "modules": ProjectModules.from_dict(obj.get("modules")) if obj.get("modules") is not None else None,
            "name": obj.get("name")
        })
        return _obj

from Pieces._pieces_lib.pieces_os_client.models.ide_tabs import IDETabs
from Pieces._pieces_lib.pieces_os_client.models.project_modules import ProjectModules
WorkstreamEventTriggerContextIDE.update_forward_refs()

