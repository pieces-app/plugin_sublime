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
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.person import Person

class SearchedPerson(BaseModel):
    """
    This is used for the Persons searching endpoint.  person here is only provided if transferables are set to true.  temporal: if this is provided this means that their material matched the input via a timestamp.  TODO will want to consider returning related materials to this material potentially both associated/ and not associated materials ie suggestion: WorkstreamSuggestions  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    person: Optional[Person] = None
    exact: StrictBool = Field(...)
    similarity: Union[StrictFloat, StrictInt] = Field(...)
    temporal: Optional[StrictBool] = None
    identifier: StrictStr = Field(default=..., description="This is the uuid of the person.")
    __properties = ["schema", "person", "exact", "similarity", "temporal", "identifier"]

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
    def from_json(cls, json_str: str) -> SearchedPerson:
        """Create an instance of SearchedPerson from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of person
        if self.person:
            _dict['person'] = self.person.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SearchedPerson:
        """Create an instance of SearchedPerson from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SearchedPerson.parse_obj(obj)

        _obj = SearchedPerson.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "person": Person.from_dict(obj.get("person")) if obj.get("person") is not None else None,
            "exact": obj.get("exact"),
            "similarity": obj.get("similarity"),
            "temporal": obj.get("temporal"),
            "identifier": obj.get("identifier")
        })
        return _obj


