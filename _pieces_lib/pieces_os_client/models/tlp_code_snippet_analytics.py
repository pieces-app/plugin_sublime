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
from Pieces._pieces_lib.pydantic import BaseModel, Field
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_fragment_classification import TLPCodeFragmentClassification
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_fragment_description import TLPCodeFragmentDescription
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_fragment_reclassification import TLPCodeFragmentReclassification
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_fragment_statistics import TLPCodeFragmentStatistics
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_fragment_tagify import TLPCodeFragmentTagify
from Pieces._pieces_lib.pieces_os_client.models.tlp_code_snippet_suggested_interactions import TLPCodeSnippetSuggestedInteractions

class TLPCodeSnippetAnalytics(BaseModel):
    """
    TLPCodeSnippetAnalytics
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    statistics: Optional[TLPCodeFragmentStatistics] = None
    classification: Optional[TLPCodeFragmentClassification] = None
    reclassification: Optional[TLPCodeFragmentReclassification] = None
    suggested: Optional[TLPCodeSnippetSuggestedInteractions] = None
    tagify: Optional[TLPCodeFragmentTagify] = None
    description: Optional[TLPCodeFragmentDescription] = None
    __properties = ["schema", "statistics", "classification", "reclassification", "suggested", "tagify", "description"]

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
    def from_json(cls, json_str: str) -> TLPCodeSnippetAnalytics:
        """Create an instance of TLPCodeSnippetAnalytics from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of statistics
        if self.statistics:
            _dict['statistics'] = self.statistics.to_dict()
        # override the default output from pydantic by calling `to_dict()` of classification
        if self.classification:
            _dict['classification'] = self.classification.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reclassification
        if self.reclassification:
            _dict['reclassification'] = self.reclassification.to_dict()
        # override the default output from pydantic by calling `to_dict()` of suggested
        if self.suggested:
            _dict['suggested'] = self.suggested.to_dict()
        # override the default output from pydantic by calling `to_dict()` of tagify
        if self.tagify:
            _dict['tagify'] = self.tagify.to_dict()
        # override the default output from pydantic by calling `to_dict()` of description
        if self.description:
            _dict['description'] = self.description.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TLPCodeSnippetAnalytics:
        """Create an instance of TLPCodeSnippetAnalytics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TLPCodeSnippetAnalytics.parse_obj(obj)

        _obj = TLPCodeSnippetAnalytics.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "statistics": TLPCodeFragmentStatistics.from_dict(obj.get("statistics")) if obj.get("statistics") is not None else None,
            "classification": TLPCodeFragmentClassification.from_dict(obj.get("classification")) if obj.get("classification") is not None else None,
            "reclassification": TLPCodeFragmentReclassification.from_dict(obj.get("reclassification")) if obj.get("reclassification") is not None else None,
            "suggested": TLPCodeSnippetSuggestedInteractions.from_dict(obj.get("suggested")) if obj.get("suggested") is not None else None,
            "tagify": TLPCodeFragmentTagify.from_dict(obj.get("tagify")) if obj.get("tagify") is not None else None,
            "description": TLPCodeFragmentDescription.from_dict(obj.get("description")) if obj.get("description") is not None else None
        })
        return _obj


