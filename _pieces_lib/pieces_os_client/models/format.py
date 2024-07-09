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
from Pieces._pieces_lib.pieces_os_client.models.activities import Activities
from Pieces._pieces_lib.pieces_os_client.models.application import Application
from Pieces._pieces_lib.pieces_os_client.models.byte_descriptor import ByteDescriptor
from Pieces._pieces_lib.pieces_os_client.models.classification import Classification
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.file_format import FileFormat
from Pieces._pieces_lib.pieces_os_client.models.flattened_asset import FlattenedAsset
from Pieces._pieces_lib.pieces_os_client.models.fragment_format import FragmentFormat
from Pieces._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from Pieces._pieces_lib.pieces_os_client.models.relationship import Relationship
from Pieces._pieces_lib.pieces_os_client.models.role import Role

class Format(BaseModel):
    """
    A representation of Data for a particular Form Factor of an Asset.  Below asset HAS to be Flattened because it is a leaf node and must prevent cycles agressively.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    id: StrictStr = Field(...)
    creator: StrictStr = Field(...)
    classification: Classification = Field(...)
    icon: Optional[StrictStr] = None
    role: Role = Field(...)
    application: Application = Field(...)
    asset: FlattenedAsset = Field(...)
    bytes: ByteDescriptor = Field(...)
    created: GroupedTimestamp = Field(...)
    updated: GroupedTimestamp = Field(...)
    deleted: Optional[GroupedTimestamp] = None
    synced: Optional[GroupedTimestamp] = None
    cloud: Optional[StrictStr] = Field(default=None, description="This is a path used to determine what path this format lives at within the cloud.")
    fragment: Optional[FragmentFormat] = None
    file: Optional[FileFormat] = None
    analysis: Optional[Analysis] = None
    relationship: Optional[Relationship] = None
    activities: Optional[Activities] = None
    __properties = ["schema", "id", "creator", "classification", "icon", "role", "application", "asset", "bytes", "created", "updated", "deleted", "synced", "cloud", "fragment", "file", "analysis", "relationship", "activities"]

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
    def from_json(cls, json_str: str) -> Format:
        """Create an instance of Format from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of classification
        if self.classification:
            _dict['classification'] = self.classification.to_dict()
        # override the default output from pydantic by calling `to_dict()` of application
        if self.application:
            _dict['application'] = self.application.to_dict()
        # override the default output from pydantic by calling `to_dict()` of asset
        if self.asset:
            _dict['asset'] = self.asset.to_dict()
        # override the default output from pydantic by calling `to_dict()` of bytes
        if self.bytes:
            _dict['bytes'] = self.bytes.to_dict()
        # override the default output from pydantic by calling `to_dict()` of created
        if self.created:
            _dict['created'] = self.created.to_dict()
        # override the default output from pydantic by calling `to_dict()` of updated
        if self.updated:
            _dict['updated'] = self.updated.to_dict()
        # override the default output from pydantic by calling `to_dict()` of deleted
        if self.deleted:
            _dict['deleted'] = self.deleted.to_dict()
        # override the default output from pydantic by calling `to_dict()` of synced
        if self.synced:
            _dict['synced'] = self.synced.to_dict()
        # override the default output from pydantic by calling `to_dict()` of fragment
        if self.fragment:
            _dict['fragment'] = self.fragment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of file
        if self.file:
            _dict['file'] = self.file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of analysis
        if self.analysis:
            _dict['analysis'] = self.analysis.to_dict()
        # override the default output from pydantic by calling `to_dict()` of relationship
        if self.relationship:
            _dict['relationship'] = self.relationship.to_dict()
        # override the default output from pydantic by calling `to_dict()` of activities
        if self.activities:
            _dict['activities'] = self.activities.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Format:
        """Create an instance of Format from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Format.parse_obj(obj)

        _obj = Format.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "id": obj.get("id"),
            "creator": obj.get("creator"),
            "classification": Classification.from_dict(obj.get("classification")) if obj.get("classification") is not None else None,
            "icon": obj.get("icon"),
            "role": obj.get("role"),
            "application": Application.from_dict(obj.get("application")) if obj.get("application") is not None else None,
            "asset": FlattenedAsset.from_dict(obj.get("asset")) if obj.get("asset") is not None else None,
            "bytes": ByteDescriptor.from_dict(obj.get("bytes")) if obj.get("bytes") is not None else None,
            "created": GroupedTimestamp.from_dict(obj.get("created")) if obj.get("created") is not None else None,
            "updated": GroupedTimestamp.from_dict(obj.get("updated")) if obj.get("updated") is not None else None,
            "deleted": GroupedTimestamp.from_dict(obj.get("deleted")) if obj.get("deleted") is not None else None,
            "synced": GroupedTimestamp.from_dict(obj.get("synced")) if obj.get("synced") is not None else None,
            "cloud": obj.get("cloud"),
            "fragment": FragmentFormat.from_dict(obj.get("fragment")) if obj.get("fragment") is not None else None,
            "file": FileFormat.from_dict(obj.get("file")) if obj.get("file") is not None else None,
            "analysis": Analysis.from_dict(obj.get("analysis")) if obj.get("analysis") is not None else None,
            "relationship": Relationship.from_dict(obj.get("relationship")) if obj.get("relationship") is not None else None,
            "activities": Activities.from_dict(obj.get("activities")) if obj.get("activities") is not None else None
        })
        return _obj

from Pieces._pieces_lib.pieces_os_client.models.analysis import Analysis
Format.update_forward_refs()

