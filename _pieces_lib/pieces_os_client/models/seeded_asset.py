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
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictBool
from Pieces._pieces_lib.pieces_os_client.models.application import Application
from Pieces._pieces_lib.pieces_os_client.models.available_formats import AvailableFormats
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.seeded_asset_enrichment import SeededAssetEnrichment
from Pieces._pieces_lib.pieces_os_client.models.seeded_asset_metadata import SeededAssetMetadata
from Pieces._pieces_lib.pieces_os_client.models.seeded_format import SeededFormat

class SeededAsset(BaseModel):
    """
    This is seed data that will be come an asset.  discovered: if set to true this seededAsset was discovered using one of our discovery endpoints.  pseudo: if this is an asset that a user did NOT explicitly save.  available: This is a model that is used within our '/assets/draft' endpoint that will emitt a seed with all the available format that one can generate based on the original seed that was passed in. ie if a png was passed in, we may  say that there is a text/code format available. If available formats is passed into the '/assets/create' we will short curcuit certain operations to speed up the process, for instance, if we determine that there is no text within this image then there is no sense in running ocr.   # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(None, alias="schema")
    metadata: Optional[SeededAssetMetadata] = None
    application: Application = Field(...)
    format: SeededFormat = Field(...)
    discovered: Optional[StrictBool] = None
    available: Optional[AvailableFormats] = None
    pseudo: Optional[StrictBool] = None
    enrichment: Optional[SeededAssetEnrichment] = None
    demo: Optional[StrictBool] = Field(None, description="This will let us know if this asset was generated as a 'demo' snippet")
    __properties = ["schema", "metadata", "application", "format", "discovered", "available", "pseudo", "enrichment", "demo"]

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
    def from_json(cls, json_str: str) -> SeededAsset:
        """Create an instance of SeededAsset from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of metadata
        if self.metadata:
            _dict['metadata'] = self.metadata.to_dict()
        # override the default output from pydantic by calling `to_dict()` of application
        if self.application:
            _dict['application'] = self.application.to_dict()
        # override the default output from pydantic by calling `to_dict()` of format
        if self.format:
            _dict['format'] = self.format.to_dict()
        # override the default output from pydantic by calling `to_dict()` of available
        if self.available:
            _dict['available'] = self.available.to_dict()
        # override the default output from pydantic by calling `to_dict()` of enrichment
        if self.enrichment:
            _dict['enrichment'] = self.enrichment.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededAsset:
        """Create an instance of SeededAsset from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededAsset.parse_obj(obj)

        _obj = SeededAsset.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "metadata": SeededAssetMetadata.from_dict(obj.get("metadata")) if obj.get("metadata") is not None else None,
            "application": Application.from_dict(obj.get("application")) if obj.get("application") is not None else None,
            "format": SeededFormat.from_dict(obj.get("format")) if obj.get("format") is not None else None,
            "discovered": obj.get("discovered"),
            "available": AvailableFormats.from_dict(obj.get("available")) if obj.get("available") is not None else None,
            "pseudo": obj.get("pseudo"),
            "enrichment": SeededAssetEnrichment.from_dict(obj.get("enrichment")) if obj.get("enrichment") is not None else None,
            "demo": obj.get("demo")
        })
        return _obj


