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


from typing import List, Optional
from Pieces._pieces_lib.pydantic import BaseModel, Field, conlist
from Pieces._pieces_lib.pieces_os_client.models.anonymous_temporal_range import AnonymousTemporalRange
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.flattened_workstream_events import FlattenedWorkstreamEvents

class AutoGeneratedWorkstreamSummaryInput(BaseModel):
    """
    This in the input body for /workstream_summaries/create/summary  throws an error if neither of events nor ranges are passed in  for now we will(XOR) ie either  1. generate based on events 2. or we will generate based on ranges  in the future we can merge these  in the future we can add 1. summaries 2. sources  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    events: Optional[FlattenedWorkstreamEvents] = None
    anonymous_ranges: Optional[conlist(AnonymousTemporalRange)] = None
    __properties = ["schema", "events", "anonymous_ranges"]

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
    def from_json(cls, json_str: str) -> AutoGeneratedWorkstreamSummaryInput:
        """Create an instance of AutoGeneratedWorkstreamSummaryInput from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of events
        if self.events:
            _dict['events'] = self.events.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in anonymous_ranges (list)
        _items = []
        if self.anonymous_ranges:
            for _item in self.anonymous_ranges:
                if _item:
                    _items.append(_item.to_dict())
            _dict['anonymous_ranges'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AutoGeneratedWorkstreamSummaryInput:
        """Create an instance of AutoGeneratedWorkstreamSummaryInput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AutoGeneratedWorkstreamSummaryInput.parse_obj(obj)

        _obj = AutoGeneratedWorkstreamSummaryInput.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "events": FlattenedWorkstreamEvents.from_dict(obj.get("events")) if obj.get("events") is not None else None,
            "anonymous_ranges": [AnonymousTemporalRange.from_dict(_item) for _item in obj.get("anonymous_ranges")] if obj.get("anonymous_ranges") is not None else None
        })
        return _obj


