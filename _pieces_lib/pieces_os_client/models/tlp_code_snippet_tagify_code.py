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
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema

class TLPCodeSnippetTagifyCode(BaseModel):
    """
      # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    distribution: StrictStr = Field(default=..., description="stringified array of numbers")
    inferred_distribution: StrictStr = Field(default=..., description="stringified array of numbers")
    tags: StrictStr = Field(default=..., description="stringified array of strings")
    inferred_tags: StrictStr = Field(default=..., description="stringified array of strings")
    model: StrictStr = Field(default=..., description="this is the model version ")
    label_version: StrictStr = Field(default=..., description="This is the version of the file that we are using that contains all the possible tags")
    threshold: Union[StrictFloat, StrictInt] = Field(default=..., description="this is the minimum score from the model that a tag needs to have to be included in the tags array.")
    inferred_threshold: Union[StrictFloat, StrictInt] = Field(default=..., description="this is the minimum score from the postprocessing that a tag needs to have to be included in the inferred_tags array.")
    context: StrictStr = Field(default=..., description="this is the origin in which this asset was created, application(string representation)")
    asset: StrictStr = Field(default=..., description="This is the asset id.")
    __properties = ["schema", "distribution", "inferred_distribution", "tags", "inferred_tags", "model", "label_version", "threshold", "inferred_threshold", "context", "asset"]

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
    def from_json(cls, json_str: str) -> TLPCodeSnippetTagifyCode:
        """Create an instance of TLPCodeSnippetTagifyCode from a JSON string"""
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
    def from_dict(cls, obj: dict) -> TLPCodeSnippetTagifyCode:
        """Create an instance of TLPCodeSnippetTagifyCode from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TLPCodeSnippetTagifyCode.parse_obj(obj)

        _obj = TLPCodeSnippetTagifyCode.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "distribution": obj.get("distribution"),
            "inferred_distribution": obj.get("inferred_distribution"),
            "tags": obj.get("tags"),
            "inferred_tags": obj.get("inferred_tags"),
            "model": obj.get("model"),
            "label_version": obj.get("label_version"),
            "threshold": obj.get("threshold"),
            "inferred_threshold": obj.get("inferred_threshold"),
            "context": obj.get("context"),
            "asset": obj.get("asset")
        })
        return _obj


