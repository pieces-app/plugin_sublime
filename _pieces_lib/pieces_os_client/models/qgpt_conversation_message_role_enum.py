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





class QGPTConversationMessageRoleEnum(str, Enum):
    """
    This is the role enum used for a QGPT conversation
    """

    """
    allowed enum values
    """
    UNKNOWN = 'UNKNOWN'
    USER = 'USER'
    SYSTEM = 'SYSTEM'
    ASSISTANT = 'ASSISTANT'

    @classmethod
    def from_json(cls, json_str: str) -> QGPTConversationMessageRoleEnum:
        """Create an instance of QGPTConversationMessageRoleEnum from a JSON string"""
        return QGPTConversationMessageRoleEnum(json.loads(json_str))


