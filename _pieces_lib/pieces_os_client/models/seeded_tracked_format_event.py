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
from Pieces._pieces_lib.pydantic import BaseModel, Field
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.tracked_format_event_identifier_description_pairs import TrackedFormatEventIdentifierDescriptionPairs
from Pieces._pieces_lib.pieces_os_client.models.tracked_format_event_metadata import TrackedFormatEventMetadata

class SeededTrackedFormatEvent(BaseModel):
    """
    Again this is a model designed to be sent over to a context server to be built and then sent along to segment.   # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    identifier_description_pair: TrackedFormatEventIdentifierDescriptionPairs = Field(...)
    format: ReferencedFormat = Field(...)
    metadata: Optional[TrackedFormatEventMetadata] = None
    __properties = ["schema", "identifier_description_pair", "format", "metadata"]

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
    def from_json(cls, json_str: str) -> SeededTrackedFormatEvent:
        """Create an instance of SeededTrackedFormatEvent from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of format
        if self.format:
            _dict['format'] = self.format.to_dict()
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededTrackedFormatEvent:
        """Create an instance of SeededTrackedFormatEvent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededTrackedFormatEvent.parse_obj(obj)

        _obj = SeededTrackedFormatEvent.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "identifier_description_pair": TrackedFormatEventIdentifierDescriptionPairs.from_dict(obj.get("identifier_description_pair")) if obj.get("identifier_description_pair") is not None else None,
            "format": ReferencedFormat.from_dict(obj.get("format")) if obj.get("format") is not None else None,
            "metadata": TrackedFormatEventMetadata.from_dict(obj.get("metadata")) if obj.get("metadata") is not None else None
        })
        return _obj

from Pieces._pieces_lib.pieces_os_client.models.referenced_format import ReferencedFormat
SeededTrackedFormatEvent.update_forward_refs()

