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
from pydantic import BaseModel, Field, StrictInt
from Pieces._pieces_lib.pieces_os_client.models.byte_descriptor import ByteDescriptor
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.workstream_pattern_engine_vision_event import WorkstreamPatternEngineVisionEvent

class WorkstreamPatternEngineVisionEventsMetadata(BaseModel):
    """
    This is specific model that will return the size of the WPE in bytes  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    bytes: ByteDescriptor = Field(...)
    total: StrictInt = Field(default=..., description="This is the total number of events.")
    oldest: Optional[WorkstreamPatternEngineVisionEvent] = None
    newest: Optional[WorkstreamPatternEngineVisionEvent] = None
    __properties = ["schema", "bytes", "total", "oldest", "newest"]

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
    def from_json(cls, json_str: str) -> WorkstreamPatternEngineVisionEventsMetadata:
        """Create an instance of WorkstreamPatternEngineVisionEventsMetadata from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of bytes
        if self.bytes:
            _dict['bytes'] = self.bytes.to_dict()
        # override the default output from pydantic by calling `to_dict()` of oldest
        if self.oldest:
            _dict['oldest'] = self.oldest.to_dict()
        # override the default output from pydantic by calling `to_dict()` of newest
        if self.newest:
            _dict['newest'] = self.newest.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WorkstreamPatternEngineVisionEventsMetadata:
        """Create an instance of WorkstreamPatternEngineVisionEventsMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WorkstreamPatternEngineVisionEventsMetadata.parse_obj(obj)

        _obj = WorkstreamPatternEngineVisionEventsMetadata.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "bytes": ByteDescriptor.from_dict(obj.get("bytes")) if obj.get("bytes") is not None else None,
            "total": obj.get("total"),
            "oldest": WorkstreamPatternEngineVisionEvent.from_dict(obj.get("oldest")) if obj.get("oldest") is not None else None,
            "newest": WorkstreamPatternEngineVisionEvent.from_dict(obj.get("newest")) if obj.get("newest") is not None else None
        })
        return _obj


