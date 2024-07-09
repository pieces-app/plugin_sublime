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
from Pieces._pieces_lib.pieces_os_client.models.seeded_workstream_event import SeededWorkstreamEvent

class SeededWorkstreamIngestion(BaseModel):
    """
    This is used as the input in the Context ingestion endpoint for the feed.  This will take in a required seed, this will get created as an internal WorkstreamEvent until we determine internally that this event is relevant and will then attach it to a WorkstreamSummary and it will get moved over to a WorkstreamEvent.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    event: SeededWorkstreamEvent = Field(...)
    __properties = ["schema", "event"]

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
    def from_json(cls, json_str: str) -> SeededWorkstreamIngestion:
        """Create an instance of SeededWorkstreamIngestion from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of event
        if self.event:
            _dict['event'] = self.event.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededWorkstreamIngestion:
        """Create an instance of SeededWorkstreamIngestion from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededWorkstreamIngestion.parse_obj(obj)

        _obj = SeededWorkstreamIngestion.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "event": SeededWorkstreamEvent.from_dict(obj.get("event")) if obj.get("event") is not None else None
        })
        return _obj


