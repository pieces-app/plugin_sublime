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
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from Pieces._pieces_lib.pieces_os_client.models.recipients import Recipients

class GitHubGistDistribution(BaseModel):
    """
    This is a published Github Gist.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    recipients: Recipients = Field(...)
    public: StrictBool = Field(default=..., description="This will let us know if the gist is public or private.")
    description: Optional[StrictStr] = Field(default=None, description="This is the description of the Gist Distribution")
    name: StrictStr = Field(default=..., description="This is the name of the gist you will add.")
    created: GroupedTimestamp = Field(...)
    updated: GroupedTimestamp = Field(...)
    deleted: Optional[GroupedTimestamp] = None
    github_id: StrictStr = Field(default=..., description="This is the id that github uses to represent the gist.")
    url: StrictStr = Field(default=..., description="This is the url where the gist is.")
    __properties = ["schema", "recipients", "public", "description", "name", "created", "updated", "deleted", "github_id", "url"]

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
    def from_json(cls, json_str: str) -> GitHubGistDistribution:
        """Create an instance of GitHubGistDistribution from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of recipients
        if self.recipients:
            _dict['recipients'] = self.recipients.to_dict()
        # override the default output from pydantic by calling `to_dict()` of created
        if self.created:
            _dict['created'] = self.created.to_dict()
        # override the default output from pydantic by calling `to_dict()` of updated
        if self.updated:
            _dict['updated'] = self.updated.to_dict()
        # override the default output from pydantic by calling `to_dict()` of deleted
        if self.deleted:
            _dict['deleted'] = self.deleted.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GitHubGistDistribution:
        """Create an instance of GitHubGistDistribution from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GitHubGistDistribution.parse_obj(obj)

        _obj = GitHubGistDistribution.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "recipients": Recipients.from_dict(obj.get("recipients")) if obj.get("recipients") is not None else None,
            "public": obj.get("public"),
            "description": obj.get("description"),
            "name": obj.get("name"),
            "created": GroupedTimestamp.from_dict(obj.get("created")) if obj.get("created") is not None else None,
            "updated": GroupedTimestamp.from_dict(obj.get("updated")) if obj.get("updated") is not None else None,
            "deleted": GroupedTimestamp.from_dict(obj.get("deleted")) if obj.get("deleted") is not None else None,
            "github_id": obj.get("github_id"),
            "url": obj.get("url")
        })
        return _obj


