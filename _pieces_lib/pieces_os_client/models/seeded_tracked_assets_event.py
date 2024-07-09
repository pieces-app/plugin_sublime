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
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.tracked_assets_event_identifier_description_pairs import TrackedAssetsEventIdentifierDescriptionPairs

class SeededTrackedAssetsEvent(BaseModel):
    """
    An seeded event model that can occur at the assets level i.e. search   # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    identifier_description_pair: Optional[TrackedAssetsEventIdentifierDescriptionPairs] = None
    metadata: Optional[SeededTrackedAssetsEventMetadata] = None
    __properties = ["schema", "identifier_description_pair", "metadata"]

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
    def from_json(cls, json_str: str) -> SeededTrackedAssetsEvent:
        """Create an instance of SeededTrackedAssetsEvent from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of identifier_description_pair
        if self.identifier_description_pair:
            _dict['identifier_description_pair'] = self.identifier_description_pair.to_dict()
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededTrackedAssetsEvent:
        """Create an instance of SeededTrackedAssetsEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededTrackedAssetsEvent.parse_obj(obj)

        _obj = SeededTrackedAssetsEvent.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "identifier_description_pair": TrackedAssetsEventIdentifierDescriptionPairs.from_dict(obj.get("identifier_description_pair")) if obj.get("identifier_description_pair") is not None else None,
            "metadata": SeededTrackedAssetsEventMetadata.from_dict(obj.get("metadata")) if obj.get("metadata") is not None else None
        })
        return _obj

from Pieces._pieces_lib.pieces_os_client.models.seeded_tracked_assets_event_metadata import SeededTrackedAssetsEventMetadata
SeededTrackedAssetsEvent.update_forward_refs()

