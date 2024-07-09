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
from Pieces._pieces_lib.pieces_os_client.models.anchor_type_enum import AnchorTypeEnum
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.flattened_anchor_points import FlattenedAnchorPoints
from Pieces._pieces_lib.pieces_os_client.models.flattened_annotations import FlattenedAnnotations
from Pieces._pieces_lib.pieces_os_client.models.flattened_assets import FlattenedAssets
from Pieces._pieces_lib.pieces_os_client.models.flattened_conversations import FlattenedConversations
from Pieces._pieces_lib.pieces_os_client.models.flattened_persons import FlattenedPersons
from Pieces._pieces_lib.pieces_os_client.models.flattened_workstream_summaries import FlattenedWorkstreamSummaries
from Pieces._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from Pieces._pieces_lib.pieces_os_client.models.score import Score

class Anchor(BaseModel):
    """
    Anchor
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    id: StrictStr = Field(...)
    name: Optional[StrictStr] = None
    type: AnchorTypeEnum = Field(...)
    watch: Optional[StrictBool] = None
    points: FlattenedAnchorPoints = Field(...)
    created: GroupedTimestamp = Field(...)
    updated: GroupedTimestamp = Field(...)
    deleted: Optional[GroupedTimestamp] = None
    assets: Optional[FlattenedAssets] = None
    annotations: Optional[FlattenedAnnotations] = None
    conversations: Optional[FlattenedConversations] = None
    score: Optional[Score] = None
    summaries: Optional[FlattenedWorkstreamSummaries] = None
    persons: Optional[FlattenedPersons] = None
    __properties = ["schema", "id", "name", "type", "watch", "points", "created", "updated", "deleted", "assets", "annotations", "conversations", "score", "summaries", "persons"]

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
    def from_json(cls, json_str: str) -> Anchor:
        """Create an instance of Anchor from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of points
        if self.points:
            _dict['points'] = self.points.to_dict()
        # override the default output from pydantic by calling `to_dict()` of created
        if self.created:
            _dict['created'] = self.created.to_dict()
        # override the default output from pydantic by calling `to_dict()` of updated
        if self.updated:
            _dict['updated'] = self.updated.to_dict()
        # override the default output from pydantic by calling `to_dict()` of deleted
        if self.deleted:
            _dict['deleted'] = self.deleted.to_dict()
        # override the default output from pydantic by calling `to_dict()` of assets
        if self.assets:
            _dict['assets'] = self.assets.to_dict()
        # override the default output from pydantic by calling `to_dict()` of annotations
        if self.annotations:
            _dict['annotations'] = self.annotations.to_dict()
        # override the default output from pydantic by calling `to_dict()` of conversations
        if self.conversations:
            _dict['conversations'] = self.conversations.to_dict()
        # override the default output from pydantic by calling `to_dict()` of score
        if self.score:
            _dict['score'] = self.score.to_dict()
        # override the default output from pydantic by calling `to_dict()` of summaries
        if self.summaries:
            _dict['summaries'] = self.summaries.to_dict()
        # override the default output from pydantic by calling `to_dict()` of persons
        if self.persons:
            _dict['persons'] = self.persons.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Anchor:
        """Create an instance of Anchor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Anchor.parse_obj(obj)

        _obj = Anchor.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "id": obj.get("id"),
            "name": obj.get("name"),
            "type": obj.get("type"),
            "watch": obj.get("watch"),
            "points": FlattenedAnchorPoints.from_dict(obj.get("points")) if obj.get("points") is not None else None,
            "created": GroupedTimestamp.from_dict(obj.get("created")) if obj.get("created") is not None else None,
            "updated": GroupedTimestamp.from_dict(obj.get("updated")) if obj.get("updated") is not None else None,
            "deleted": GroupedTimestamp.from_dict(obj.get("deleted")) if obj.get("deleted") is not None else None,
            "assets": FlattenedAssets.from_dict(obj.get("assets")) if obj.get("assets") is not None else None,
            "annotations": FlattenedAnnotations.from_dict(obj.get("annotations")) if obj.get("annotations") is not None else None,
            "conversations": FlattenedConversations.from_dict(obj.get("conversations")) if obj.get("conversations") is not None else None,
            "score": Score.from_dict(obj.get("score")) if obj.get("score") is not None else None,
            "summaries": FlattenedWorkstreamSummaries.from_dict(obj.get("summaries")) if obj.get("summaries") is not None else None,
            "persons": FlattenedPersons.from_dict(obj.get("persons")) if obj.get("persons") is not None else None
        })
        return _obj


