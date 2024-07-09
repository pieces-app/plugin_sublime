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
from Pieces._pieces_lib.pieces_os_client.models.browser_selection import BrowserSelection
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.transferable_string import TransferableString

class BrowserTabValue(BaseModel):
    """
    snippet: these are extracted code blocks selection: here is a copy/paste/selection  note: recommended that you pass in the md version of the webpage  note: please dont pass in all three html,md,text, just pass in 1.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    html: Optional[TransferableString] = None
    md: Optional[TransferableString] = None
    text: Optional[TransferableString] = None
    snippet: Optional[BrowserSelection] = None
    selection: Optional[BrowserSelection] = None
    __properties = ["schema", "html", "md", "text", "snippet", "selection"]

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
    def from_json(cls, json_str: str) -> BrowserTabValue:
        """Create an instance of BrowserTabValue from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of html
        if self.html:
            _dict['html'] = self.html.to_dict()
        # override the default output from pydantic by calling `to_dict()` of md
        if self.md:
            _dict['md'] = self.md.to_dict()
        # override the default output from pydantic by calling `to_dict()` of text
        if self.text:
            _dict['text'] = self.text.to_dict()
        # override the default output from pydantic by calling `to_dict()` of snippet
        if self.snippet:
            _dict['snippet'] = self.snippet.to_dict()
        # override the default output from pydantic by calling `to_dict()` of selection
        if self.selection:
            _dict['selection'] = self.selection.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BrowserTabValue:
        """Create an instance of BrowserTabValue from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BrowserTabValue.parse_obj(obj)

        _obj = BrowserTabValue.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "html": TransferableString.from_dict(obj.get("html")) if obj.get("html") is not None else None,
            "md": TransferableString.from_dict(obj.get("md")) if obj.get("md") is not None else None,
            "text": TransferableString.from_dict(obj.get("text")) if obj.get("text") is not None else None,
            "snippet": BrowserSelection.from_dict(obj.get("snippet")) if obj.get("snippet") is not None else None,
            "selection": BrowserSelection.from_dict(obj.get("selection")) if obj.get("selection") is not None else None
        })
        return _obj


