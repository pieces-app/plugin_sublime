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
from pydantic import BaseModel, Field, StrictBool, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.asset_filters import AssetFilters
from Pieces._pieces_lib.pieces_os_client.models.asset_search_space import AssetSearchSpace
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class AssetsSearchWithFiltersInput(BaseModel):
    """
    AssetsSearchWithFiltersInput
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    query: Optional[StrictStr] = None
    space: Optional[AssetSearchSpace] = None
    filters: Optional[AssetFilters] = None
    casing: Optional[StrictBool] = Field(default=None, description="This is an optional bool that will let us know, if we want to ignore case or not.(default is to allow casing)ie casing:true.")
    __properties = ["schema", "query", "space", "filters", "casing"]

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
    def from_json(cls, json_str: str) -> AssetsSearchWithFiltersInput:
        """Create an instance of AssetsSearchWithFiltersInput from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of space
        if self.space:
            _dict['space'] = self.space.to_dict()
        # override the default output from pydantic by calling `to_dict()` of filters
        if self.filters:
            _dict['filters'] = self.filters.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AssetsSearchWithFiltersInput:
        """Create an instance of AssetsSearchWithFiltersInput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AssetsSearchWithFiltersInput.parse_obj(obj)

        _obj = AssetsSearchWithFiltersInput.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "query": obj.get("query"),
            "space": AssetSearchSpace.from_dict(obj.get("space")) if obj.get("space") is not None else None,
            "filters": AssetFilters.from_dict(obj.get("filters")) if obj.get("filters") is not None else None,
            "casing": obj.get("casing")
        })
        return _obj


