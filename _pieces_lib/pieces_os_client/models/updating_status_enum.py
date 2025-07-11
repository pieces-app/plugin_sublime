# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from Pieces._pieces_lib.aenum import Enum, no_arg





class UpdatingStatusEnum(str, Enum):
    """
    This is a simple enum used to determine the status of the Updating process.(of PiecesOS)  UpdatingStatusEnum(READY_TO_RESTART, AVAILABLE(but not downloaded), DOWNLOADING, UNKNOWN, UP_TO_DATE)  UNKNOWN: should never be the case  These are some enums that are currently not implemented but are for future support( REINSTALL_REQUIRED, CONTACT_SUPPORT)
    """

    """
    allowed enum values
    """
    UNKNOWN = 'UNKNOWN'
    READY_TO_RESTART = 'READY_TO_RESTART'
    AVAILABLE = 'AVAILABLE'
    DOWNLOADING = 'DOWNLOADING'
    UP_TO_DATE = 'UP_TO_DATE'
    REINSTALL_REQUIRED = 'REINSTALL_REQUIRED'
    CONTACT_SUPPORT = 'CONTACT_SUPPORT'

    @classmethod
    def from_json(cls, json_str: str) -> UpdatingStatusEnum:
        """Create an instance of UpdatingStatusEnum from a JSON string"""
        return UpdatingStatusEnum(json.loads(json_str))


