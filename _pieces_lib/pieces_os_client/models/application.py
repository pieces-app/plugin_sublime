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
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictBool, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.application_name_enum import ApplicationNameEnum
from Pieces._pieces_lib.pieces_os_client.models.capabilities_enum import CapabilitiesEnum
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.mechanism_enum import MechanismEnum
from Pieces._pieces_lib.pieces_os_client.models.platform_enum import PlatformEnum
from Pieces._pieces_lib.pieces_os_client.models.privacy_enum import PrivacyEnum
from Pieces._pieces_lib.pieces_os_client.models.seeded_asset_enrichment import SeededAssetEnrichment

class Application(BaseModel):
    """
    A Model to describe what application a format/analytics event originated.  mechanism: This will let us know where this came from. ie.only 2 enums are used here or else throw and error. default mechanism here is MANUAL- meaning that this came from our user Connecting an application. INTERNAL - means that this came from a shareable link  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    id: StrictStr = Field(default=..., description="The ID of the application at the device level")
    name: ApplicationNameEnum = Field(...)
    version: StrictStr = Field(default=..., description="This is the specific version number 0.0.0")
    platform: PlatformEnum = Field(...)
    onboarded: StrictBool = Field(...)
    privacy: PrivacyEnum = Field(...)
    capabilities: Optional[CapabilitiesEnum] = None
    mechanism: Optional[MechanismEnum] = None
    automatic_unload: Optional[StrictBool] = Field(default=None, alias="automaticUnload", description="This is a proper that will let us know if we will proactivity unload all of your machine learning models.by default this is false.")
    enrichment: Optional[SeededAssetEnrichment] = None
    __properties = ["schema", "id", "name", "version", "platform", "onboarded", "privacy", "capabilities", "mechanism", "automaticUnload", "enrichment"]

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
    def from_json(cls, json_str: str) -> Application:
        """Create an instance of Application from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of enrichment
        if self.enrichment:
            _dict['enrichment'] = self.enrichment.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Application:
        """Create an instance of Application from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Application.parse_obj(obj)

        _obj = Application.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "id": obj.get("id"),
            "name": obj.get("name"),
            "version": obj.get("version"),
            "platform": obj.get("platform"),
            "onboarded": obj.get("onboarded"),
            "privacy": obj.get("privacy"),
            "capabilities": obj.get("capabilities"),
            "mechanism": obj.get("mechanism"),
            "automatic_unload": obj.get("automaticUnload"),
            "enrichment": SeededAssetEnrichment.from_dict(obj.get("enrichment")) if obj.get("enrichment") is not None else None
        })
        return _obj


