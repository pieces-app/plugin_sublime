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
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from Pieces._pieces_lib.pieces_os_client.models.byte_descriptor import ByteDescriptor
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.external_ml_provider_enum import ExternalMLProviderEnum
from Pieces._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from Pieces._pieces_lib.pieces_os_client.models.model_foundation_enum import ModelFoundationEnum
from Pieces._pieces_lib.pieces_os_client.models.model_max_tokens import ModelMaxTokens
from Pieces._pieces_lib.pieces_os_client.models.model_type_enum import ModelTypeEnum
from Pieces._pieces_lib.pieces_os_client.models.model_usage_enum import ModelUsageEnum

class Model(BaseModel):
    """
    This is a Machine Learning Model, that will give readable information about the Machine Learning Model Used.  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    id: StrictStr = Field(default=..., description="uuid ")
    version: StrictStr = Field(default=..., description="this is a version of the model.")
    created: GroupedTimestamp = Field(...)
    name: StrictStr = Field(default=..., description="This is an Optional Name of the Model.")
    description: Optional[StrictStr] = Field(default=None, description="An Optional Description of the model itself.")
    cloud: StrictBool = Field(default=..., description="This will inform the user if this was a model that is hosted in the cloud")
    type: ModelTypeEnum = Field(...)
    usage: ModelUsageEnum = Field(...)
    bytes: Optional[ByteDescriptor] = None
    ram: Optional[ByteDescriptor] = None
    quantization: Optional[StrictStr] = Field(default=None, description="quantization is a string like: q8f16_0,  q4f16_1, etc...")
    foundation: Optional[ModelFoundationEnum] = None
    downloaded: Optional[StrictBool] = Field(default=None, description="This is an optional bool to let us know if this model has been downloaded locally.")
    loaded: Optional[StrictBool] = Field(default=None, description="This is a boolean that represents if the model is loaded into memory.(this is not persisted, and is calculated on the fly.)")
    unique: Optional[StrictStr] = Field(default=None, description="This is the unique model name used to load the model.")
    parameters: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="This is the number of parameters in terms of billions.")
    provider: Optional[ExternalMLProviderEnum] = None
    cpu: Optional[StrictBool] = Field(default=None, description="This is an optional bool that is optimized for CPU usage.")
    downloading: Optional[StrictBool] = Field(default=None, description="This is a calculated property, that will say if this is currently downloading.")
    max_tokens: Optional[ModelMaxTokens] = Field(default=None, alias="maxTokens")
    custom: Optional[StrictBool] = None
    __properties = ["schema", "id", "version", "created", "name", "description", "cloud", "type", "usage", "bytes", "ram", "quantization", "foundation", "downloaded", "loaded", "unique", "parameters", "provider", "cpu", "downloading", "maxTokens", "custom"]

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
    def from_json(cls, json_str: str) -> Model:
        """Create an instance of Model from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of created
        if self.created:
            _dict['created'] = self.created.to_dict()
        # override the default output from pydantic by calling `to_dict()` of bytes
        if self.bytes:
            _dict['bytes'] = self.bytes.to_dict()
        # override the default output from pydantic by calling `to_dict()` of ram
        if self.ram:
            _dict['ram'] = self.ram.to_dict()
        # override the default output from pydantic by calling `to_dict()` of max_tokens
        if self.max_tokens:
            _dict['maxTokens'] = self.max_tokens.to_dict()
        # set to None if parameters (nullable) is None
        # and __fields_set__ contains the field
        if self.parameters is None and "parameters" in self.__fields_set__:
            _dict['parameters'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Model:
        """Create an instance of Model from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Model.parse_obj(obj)

        _obj = Model.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "id": obj.get("id"),
            "version": obj.get("version"),
            "created": GroupedTimestamp.from_dict(obj.get("created")) if obj.get("created") is not None else None,
            "name": obj.get("name"),
            "description": obj.get("description"),
            "cloud": obj.get("cloud"),
            "type": obj.get("type"),
            "usage": obj.get("usage"),
            "bytes": ByteDescriptor.from_dict(obj.get("bytes")) if obj.get("bytes") is not None else None,
            "ram": ByteDescriptor.from_dict(obj.get("ram")) if obj.get("ram") is not None else None,
            "quantization": obj.get("quantization"),
            "foundation": obj.get("foundation"),
            "downloaded": obj.get("downloaded"),
            "loaded": obj.get("loaded"),
            "unique": obj.get("unique"),
            "parameters": obj.get("parameters"),
            "provider": obj.get("provider"),
            "cpu": obj.get("cpu"),
            "downloading": obj.get("downloading"),
            "max_tokens": ModelMaxTokens.from_dict(obj.get("maxTokens")) if obj.get("maxTokens") is not None else None,
            "custom": obj.get("custom")
        })
        return _obj


