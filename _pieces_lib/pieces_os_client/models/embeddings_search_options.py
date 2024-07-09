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


from typing import Optional, Union
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictFloat, StrictInt
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.embeddings_search_options_embedding_type_enum import EmbeddingsSearchOptionsEmbeddingTypeEnum

class EmbeddingsSearchOptions(BaseModel):
    """
    similarity: this is optional from 0 - 1, (where 1 is exact and 0 is everything)  TODO consider a plural of types for running many embedding search scopes  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    type: EmbeddingsSearchOptionsEmbeddingTypeEnum = Field(...)
    similarity: Optional[Union[StrictFloat, StrictInt]] = None
    __properties = ["schema", "type", "similarity"]

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
    def from_json(cls, json_str: str) -> EmbeddingsSearchOptions:
        """Create an instance of EmbeddingsSearchOptions from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> EmbeddingsSearchOptions:
        """Create an instance of EmbeddingsSearchOptions from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return EmbeddingsSearchOptions.parse_obj(obj)

        _obj = EmbeddingsSearchOptions.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "type": obj.get("type"),
            "similarity": obj.get("similarity")
        })
        return _obj


