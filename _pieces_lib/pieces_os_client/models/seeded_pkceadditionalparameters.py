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
from Pieces._pieces_lib.pydantic import BaseModel, StrictStr, validator

class SeededPKCEADDITIONALPARAMETERS(BaseModel):
    """
    Append any additional parameter to the end of your request, and it will be sent to the provider. For example, access_type=offline (for Google Refresh Tokens) , display=popup (for Windows Live popup mode).  # noqa: E501
    """
    access_type: Optional[StrictStr] = 'UNKNOWN'
    display: Optional[StrictStr] = 'UNKNOWN'
    __properties = ["access_type", "display"]

    @validator('access_type')
    def access_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('UNKNOWN', 'offline',):
            raise ValueError("must be one of enum values ('UNKNOWN', 'offline')")
        return value

    @validator('display')
    def display_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('UNKNOWN', 'popup',):
            raise ValueError("must be one of enum values ('UNKNOWN', 'popup')")
        return value

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
    def from_json(cls, json_str: str) -> SeededPKCEADDITIONALPARAMETERS:
        """Create an instance of SeededPKCEADDITIONALPARAMETERS from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededPKCEADDITIONALPARAMETERS:
        """Create an instance of SeededPKCEADDITIONALPARAMETERS from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededPKCEADDITIONALPARAMETERS.parse_obj(obj)

        _obj = SeededPKCEADDITIONALPARAMETERS.parse_obj({
            "access_type": obj.get("access_type") if obj.get("access_type") is not None else 'UNKNOWN',
            "display": obj.get("display") if obj.get("display") is not None else 'UNKNOWN'
        })
        return _obj


