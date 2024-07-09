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
from Pieces._pieces_lib.pieces_os_client.models.seeded_classification import SeededClassification
from Pieces._pieces_lib.pieces_os_client.models.seeded_file import SeededFile
from Pieces._pieces_lib.pieces_os_client.models.seeded_fragment import SeededFragment

class SeededFormat(BaseModel):
    """
    This is seeded data that will be come a format.  We will throw an Error if, 1) file and fragment are both defined, 2) file and fragment are both null.  if this is being used within the /assets/create endpoint or the /{application}/create endpoint, we will not take the classificaiton into account, as it is only used in the syntax highlighting related endpoints.That being said if you do want to override your classification, please look at the metadata within the file or the fragment.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    file: Optional[SeededFile] = None
    fragment: Optional[SeededFragment] = None
    classification: Optional[SeededClassification] = None
    __properties = ["schema", "file", "fragment", "classification"]

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
    def from_json(cls, json_str: str) -> SeededFormat:
        """Create an instance of SeededFormat from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of file
        if self.file:
            _dict['file'] = self.file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of fragment
        if self.fragment:
            _dict['fragment'] = self.fragment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of classification
        if self.classification:
            _dict['classification'] = self.classification.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededFormat:
        """Create an instance of SeededFormat from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededFormat.parse_obj(obj)

        _obj = SeededFormat.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "file": SeededFile.from_dict(obj.get("file")) if obj.get("file") is not None else None,
            "fragment": SeededFragment.from_dict(obj.get("fragment")) if obj.get("fragment") is not None else None,
            "classification": SeededClassification.from_dict(obj.get("classification")) if obj.get("classification") is not None else None
        })
        return _obj


