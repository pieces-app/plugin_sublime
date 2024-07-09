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
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from Pieces._pieces_lib.pieces_os_client.models.qgpt_conversation_message_role_enum import QGPTConversationMessageRoleEnum

class QGPTConversationMessage(BaseModel):
    """
    This will take a single message, and a role.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    text: StrictStr = Field(...)
    role: QGPTConversationMessageRoleEnum = Field(...)
    timestamp: GroupedTimestamp = Field(...)
    __properties = ["schema", "text", "role", "timestamp"]

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
    def from_json(cls, json_str: str) -> QGPTConversationMessage:
        """Create an instance of QGPTConversationMessage from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of timestamp
        if self.timestamp:
            _dict['timestamp'] = self.timestamp.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> QGPTConversationMessage:
        """Create an instance of QGPTConversationMessage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return QGPTConversationMessage.parse_obj(obj)

        _obj = QGPTConversationMessage.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "text": obj.get("text"),
            "role": obj.get("role"),
            "timestamp": GroupedTimestamp.from_dict(obj.get("timestamp")) if obj.get("timestamp") is not None else None
        })
        return _obj


