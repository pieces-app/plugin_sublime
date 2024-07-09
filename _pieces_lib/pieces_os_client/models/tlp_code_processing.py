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
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_directory_analytics import TLPCodeDirectoryAnalytics
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_file_analytics import TLPCodeFileAnalytics
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_repository_analytics import TLPCodeRepositoryAnalytics
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_snippet_analytics import TLPCodeSnippetAnalytics

class TLPCodeProcessing(BaseModel):
    """
    TLPCodeProcessing
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    fragment: Optional[TLPCodeSnippetAnalytics] = None
    file: Optional[TLPCodeFileAnalytics] = None
    directory: Optional[TLPCodeDirectoryAnalytics] = None
    repository: Optional[TLPCodeRepositoryAnalytics] = None
    __properties = ["schema", "fragment", "file", "directory", "repository"]

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
    def from_json(cls, json_str: str) -> TLPCodeProcessing:
        """Create an instance of TLPCodeProcessing from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of fragment
        if self.fragment:
            _dict['fragment'] = self.fragment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of file
        if self.file:
            _dict['file'] = self.file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of directory
        if self.directory:
            _dict['directory'] = self.directory.to_dict()
        # override the default output from pydantic by calling `to_dict()` of repository
        if self.repository:
            _dict['repository'] = self.repository.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TLPCodeProcessing:
        """Create an instance of TLPCodeProcessing from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TLPCodeProcessing.parse_obj(obj)

        _obj = TLPCodeProcessing.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "fragment": TLPCodeSnippetAnalytics.from_dict(obj.get("fragment")) if obj.get("fragment") is not None else None,
            "file": TLPCodeFileAnalytics.from_dict(obj.get("file")) if obj.get("file") is not None else None,
            "directory": TLPCodeDirectoryAnalytics.from_dict(obj.get("directory")) if obj.get("directory") is not None else None,
            "repository": TLPCodeRepositoryAnalytics.from_dict(obj.get("repository")) if obj.get("repository") is not None else None
        })
        return _obj


