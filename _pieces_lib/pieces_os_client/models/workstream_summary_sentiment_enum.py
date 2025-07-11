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





class WorkstreamSummarySentimentEnum(str, Enum):
    """
    This will describe the sentiment of a specific summary ie if the summary was liked/disliked/reported
    """

    """
    allowed enum values
    """
    UNKNOWN = 'UNKNOWN'
    LIKE = 'LIKE'
    DISLIKE = 'DISLIKE'
    REPORT = 'REPORT'

    @classmethod
    def from_json(cls, json_str: str) -> WorkstreamSummarySentimentEnum:
        """Create an instance of WorkstreamSummarySentimentEnum from a JSON string"""
        return WorkstreamSummarySentimentEnum(json.loads(json_str))


