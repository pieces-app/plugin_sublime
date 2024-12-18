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


from typing import List, Optional
from Pieces._pieces_lib.pydantic import BaseModel, Field, conlist
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.os_device_cpu_hardware_information import OSDeviceCPUHardwareInformation
from Pieces._pieces_lib.pieces_os_client.models.os_device_gpu_hardware_information import OSDeviceGPUHardwareInformation
from Pieces._pieces_lib.pieces_os_client.models.os_device_ram_hardware_information import OSDeviceRAMHardwareInformation

class OSDeviceHardwareInformation(BaseModel):
    """
    this will let us know specific hardware information  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    cpus: Optional[conlist(OSDeviceCPUHardwareInformation)] = None
    gpus: Optional[conlist(OSDeviceGPUHardwareInformation)] = None
    ram: Optional[OSDeviceRAMHardwareInformation] = None
    __properties = ["schema", "cpus", "gpus", "ram"]

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
    def from_json(cls, json_str: str) -> OSDeviceHardwareInformation:
        """Create an instance of OSDeviceHardwareInformation from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in cpus (list)
        _items = []
        if self.cpus:
            for _item in self.cpus:
                if _item:
                    _items.append(_item.to_dict())
            _dict['cpus'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in gpus (list)
        _items = []
        if self.gpus:
            for _item in self.gpus:
                if _item:
                    _items.append(_item.to_dict())
            _dict['gpus'] = _items
        # override the default output from pydantic by calling `to_dict()` of ram
        if self.ram:
            _dict['ram'] = self.ram.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OSDeviceHardwareInformation:
        """Create an instance of OSDeviceHardwareInformation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OSDeviceHardwareInformation.parse_obj(obj)

        _obj = OSDeviceHardwareInformation.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "cpus": [OSDeviceCPUHardwareInformation.from_dict(_item) for _item in obj.get("cpus")] if obj.get("cpus") is not None else None,
            "gpus": [OSDeviceGPUHardwareInformation.from_dict(_item) for _item in obj.get("gpus")] if obj.get("gpus") is not None else None,
            "ram": OSDeviceRAMHardwareInformation.from_dict(obj.get("ram")) if obj.get("ram") is not None else None
        })
        return _obj


