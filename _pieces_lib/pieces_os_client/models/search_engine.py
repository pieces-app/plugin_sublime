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
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.embeddings_search_options import EmbeddingsSearchOptions
from Pieces._pieces_lib.pieces_os_client.models.full_text_search_options import FullTextSearchOptions
from Pieces._pieces_lib.pieces_os_client.models.temporal_search_options import TemporalSearchOptions
from Pieces._pieces_lib.pieces_os_client.models.workstream_search_options import WorkstreamSearchOptions

class SearchEngine(BaseModel):
    """
    This will determine the type of search that will run  These are all different searching methods all of which are exclusive. Meaning that you cannot mix & match types.  operations: is here if you want to build complex searching behavior. (A || B) && (B || C) , note this can get very complex but can be as flexible as you need.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    query: Optional[StrictStr] = None
    embeddings: Optional[EmbeddingsSearchOptions] = None
    full_text: Optional[FullTextSearchOptions] = None
    temporal: Optional[TemporalSearchOptions] = None
    workstream: Optional[WorkstreamSearchOptions] = None
    operations: Optional[SearchEngines] = None
    __properties = ["schema", "query", "embeddings", "full_text", "temporal", "workstream", "operations"]

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
    def from_json(cls, json_str: str) -> SearchEngine:
        """Create an instance of SearchEngine from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of embeddings
        if self.embeddings:
            _dict['embeddings'] = self.embeddings.to_dict()
        # override the default output from pydantic by calling `to_dict()` of full_text
        if self.full_text:
            _dict['full_text'] = self.full_text.to_dict()
        # override the default output from pydantic by calling `to_dict()` of temporal
        if self.temporal:
            _dict['temporal'] = self.temporal.to_dict()
        # override the default output from pydantic by calling `to_dict()` of workstream
        if self.workstream:
            _dict['workstream'] = self.workstream.to_dict()
        # override the default output from pydantic by calling `to_dict()` of operations
        if self.operations:
            _dict['operations'] = self.operations.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SearchEngine:
        """Create an instance of SearchEngine from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SearchEngine.parse_obj(obj)

        _obj = SearchEngine.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "query": obj.get("query"),
            "embeddings": EmbeddingsSearchOptions.from_dict(obj.get("embeddings")) if obj.get("embeddings") is not None else None,
            "full_text": FullTextSearchOptions.from_dict(obj.get("full_text")) if obj.get("full_text") is not None else None,
            "temporal": TemporalSearchOptions.from_dict(obj.get("temporal")) if obj.get("temporal") is not None else None,
            "workstream": WorkstreamSearchOptions.from_dict(obj.get("workstream")) if obj.get("workstream") is not None else None,
            "operations": SearchEngines.from_dict(obj.get("operations")) if obj.get("operations") is not None else None
        })
        return _obj

from Pieces._pieces_lib.pieces_os_client.models.search_engines import SearchEngines
SearchEngine.update_forward_refs()
