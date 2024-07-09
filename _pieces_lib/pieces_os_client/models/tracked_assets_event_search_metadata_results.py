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
from pydantic import BaseModel, Field, StrictFloat, StrictInt
from Pieces._pieces_lib.pieces_os_client.models.space import Space

class TrackedAssetsEventSearchMetadataResults(BaseModel):
    """
    Numbers related to search results  # noqa: E501
    """
    fuzzy: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Total number of fuzzy results")
    exact: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Total number of exact results")
    assets: Optional[FlattenedAssets] = None
    space: Optional[Space] = None
    __properties = ["fuzzy", "exact", "assets", "space"]

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
    def from_json(cls, json_str: str) -> TrackedAssetsEventSearchMetadataResults:
        """Create an instance of TrackedAssetsEventSearchMetadataResults from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of assets
        if self.assets:
            _dict['assets'] = self.assets.to_dict()
        # override the default output from pydantic by calling `to_dict()` of space
        if self.space:
            _dict['space'] = self.space.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TrackedAssetsEventSearchMetadataResults:
        """Create an instance of TrackedAssetsEventSearchMetadataResults from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TrackedAssetsEventSearchMetadataResults.parse_obj(obj)

        _obj = TrackedAssetsEventSearchMetadataResults.parse_obj({
            "fuzzy": obj.get("fuzzy"),
            "exact": obj.get("exact"),
            "assets": FlattenedAssets.from_dict(obj.get("assets")) if obj.get("assets") is not None else None,
            "space": Space.from_dict(obj.get("space")) if obj.get("space") is not None else None
        })
        return _obj

from Pieces._pieces_lib.pieces_os_client.models.flattened_assets import FlattenedAssets
TrackedAssetsEventSearchMetadataResults.update_forward_refs()

