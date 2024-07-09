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
from aenum import Enum, no_arg





class ExternalMLProviderEnum(str, Enum):
    """
    This is a Model used for the Model class. This will be used to describe the provider in which this Mode lcam from IE meta, google, apple, ...etc
    """

    """
    allowed enum values
    """
    APPLE = 'APPLE'
    AMAZON = 'AMAZON'
    GOOGLE = 'GOOGLE'
    META = 'META'
    OPENAI = 'OPENAI'
    LMSYS = 'LMSYS'
    SALESFORCE = 'SALESFORCE'
    HUGGING_FACE = 'HUGGING_FACE'
    UNIVERSITY_OF_WASHINGTON = 'UNIVERSITY_OF_WASHINGTON'
    OPEN_LM_RESEARCH = 'OPEN_LM_RESEARCH'
    MICROSOFT = 'MICROSOFT'
    UC_BERKLEY = 'UC_BERKLEY'
    PEKING_UNIVERSITY = 'PEKING_UNIVERSITY'
    RENMIN_UNIVERSITY_OF_CHINA = 'RENMIN_UNIVERSITY_OF_CHINA'
    TOGETHER_AI = 'TOGETHER_AI'
    DATABRICKS = 'DATABRICKS'
    ELEUTHER_AI = 'ELEUTHER_AI'
    FUDAN_UNIVERSITY = 'FUDAN_UNIVERSITY'
    BLICKDL = 'BLICKDL'
    HONG_KONG_BAPTIST_UNIVERSITY = 'HONG_KONG_BAPTIST_UNIVERSITY'
    BIGCODE = 'BIGCODE'
    JINA = 'JINA'
    PIECES = 'PIECES'
    ANTHROPIC = 'ANTHROPIC'
    IBM = 'IBM'
    SNOWFLAKE = 'SNOWFLAKE'
    PERPLEXITY = 'PERPLEXITY'

    @classmethod
    def from_json(cls, json_str: str) -> ExternalMLProviderEnum:
        """Create an instance of ExternalMLProviderEnum from a JSON string"""
        return ExternalMLProviderEnum(json.loads(json_str))


