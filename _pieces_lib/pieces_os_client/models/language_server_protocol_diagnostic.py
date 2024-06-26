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
from Pieces._pieces_lib.pieces_os_client.models.language_server_protocol_code import LanguageServerProtocolCode
from Pieces._pieces_lib.pieces_os_client.models.language_server_protocol_code_description import LanguageServerProtocolCodeDescription
from Pieces._pieces_lib.pieces_os_client.models.language_server_protocol_location_range import LanguageServerProtocolLocationRange
from Pieces._pieces_lib.pieces_os_client.models.language_server_protocol_severity_enum import LanguageServerProtocolSeverityEnum

class LanguageServerProtocolDiagnostic(BaseModel):
    """
    TODO  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(None, alias="schema")
    range: LanguageServerProtocolLocationRange = Field(...)
    severity: Optional[LanguageServerProtocolSeverityEnum] = None
    code: Optional[LanguageServerProtocolCode] = None
    code_description: Optional[LanguageServerProtocolCodeDescription] = Field(None, alias="codeDescription")
    source: Optional[StrictStr] = None
    message: StrictStr = Field(...)
    __properties = ["schema", "range", "severity", "code", "codeDescription", "source", "message"]

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
    def from_json(cls, json_str: str) -> LanguageServerProtocolDiagnostic:
        """Create an instance of LanguageServerProtocolDiagnostic from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of range
        if self.range:
            _dict['range'] = self.range.to_dict()
        # override the default output from pydantic by calling `to_dict()` of code
        if self.code:
            _dict['code'] = self.code.to_dict()
        # override the default output from pydantic by calling `to_dict()` of code_description
        if self.code_description:
            _dict['codeDescription'] = self.code_description.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LanguageServerProtocolDiagnostic:
        """Create an instance of LanguageServerProtocolDiagnostic from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LanguageServerProtocolDiagnostic.parse_obj(obj)

        _obj = LanguageServerProtocolDiagnostic.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "range": LanguageServerProtocolLocationRange.from_dict(obj.get("range")) if obj.get("range") is not None else None,
            "severity": obj.get("severity"),
            "code": LanguageServerProtocolCode.from_dict(obj.get("code")) if obj.get("code") is not None else None,
            "code_description": LanguageServerProtocolCodeDescription.from_dict(obj.get("codeDescription")) if obj.get("codeDescription") is not None else None,
            "source": obj.get("source"),
            "message": obj.get("message")
        })
        return _obj


