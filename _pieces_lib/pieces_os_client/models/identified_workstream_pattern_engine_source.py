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


from typing import List, Optional, Union
from Pieces._pieces_lib.pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, conlist
from Pieces._pieces_lib.pieces_os_client.models.embedded_model_schema import EmbeddedModelSchema
from Pieces._pieces_lib.pieces_os_client.models.flattened_anchors import FlattenedAnchors
from Pieces._pieces_lib.pieces_os_client.models.flattened_conversation_messages import FlattenedConversationMessages
from Pieces._pieces_lib.pieces_os_client.models.flattened_conversations import FlattenedConversations
from Pieces._pieces_lib.pieces_os_client.models.flattened_persons import FlattenedPersons
from Pieces._pieces_lib.pieces_os_client.models.flattened_websites import FlattenedWebsites
from Pieces._pieces_lib.pieces_os_client.models.flattened_workstream_events import FlattenedWorkstreamEvents
from Pieces._pieces_lib.pieces_os_client.models.flattened_workstream_summaries import FlattenedWorkstreamSummaries
from Pieces._pieces_lib.pieces_os_client.models.grouped_timestamp import GroupedTimestamp
from Pieces._pieces_lib.pieces_os_client.models.score import Score
from Pieces._pieces_lib.pieces_os_client.models.workstream_pattern_engine_source import WorkstreamPatternEngineSource
from Pieces._pieces_lib.pieces_os_client.models.workstream_pattern_engine_source_supported_accessibility import WorkstreamPatternEngineSourceSupportedAccessibility

class IdentifiedWorkstreamPatternEngineSource(BaseModel):
    """
    This is a specific persisted model for WorkstreamPatternEngineSources that are persisted in the database(not just on the WPE event)  note: there is a \"WorkstreamPatternEngineSource\" model however we will NOT be modify this because it is linked to a different model that would require additional code to properly associate/disassociate.  note: we get 3 raw events from the WPE data so far:(encapsulated in the \"WorkstreamPatternEngineSource\") event 1. (deprecated) browserUrl - defaults to null 2. appTitle - ** not sure on default here ** (this is because this is always present on all WPE events.) 3. (deprecated) windowTitle - defaults to \"Window Title Not Found\"  NOTE we will no longer support adding window title and browser url on the source it will be generic(we will next update this to include these associations)  note: raw is the raw value from the WPE(expect I will replace the defaults w/ nullish values)  # noqa: E501
    """
    var_schema: Optional[EmbeddedModelSchema] = Field(default=None, alias="schema")
    id: StrictStr = Field(...)
    raw: WorkstreamPatternEngineSource = Field(...)
    created: GroupedTimestamp = Field(...)
    updated: GroupedTimestamp = Field(...)
    filter: Optional[StrictBool] = Field(default=None, description="This will determine if we want to filter this specific source")
    score: Optional[Score] = None
    readable: StrictStr = Field(default=..., description="This is the name of the source(defualt original data) this is NOT used for matching just for readability")
    summaries: Optional[FlattenedWorkstreamSummaries] = None
    workstream_events: Optional[FlattenedWorkstreamEvents] = None
    conversations: Optional[FlattenedConversations] = None
    accessibility: Optional[WorkstreamPatternEngineSourceSupportedAccessibility] = None
    messages: Optional[FlattenedConversationMessages] = None
    websites: Optional[FlattenedWebsites] = None
    anchors: Optional[FlattenedAnchors] = None
    persons: Optional[FlattenedPersons] = None
    workstream_pattern_engine_sources_vector: Optional[conlist(Union[StrictFloat, StrictInt])] = Field(default=None, alias="workstreamPatternEngineSourcesVector", description="This is the embedding for the wpeSource.(NEEDs to collectionection.vector) and specific here because we can only index on a single name NOTE: this the the vector index that corresponds the the couchbase lite index.")
    __properties = ["schema", "id", "raw", "created", "updated", "filter", "score", "readable", "summaries", "workstream_events", "conversations", "accessibility", "messages", "websites", "anchors", "persons", "workstreamPatternEngineSourcesVector"]

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
    def from_json(cls, json_str: str) -> IdentifiedWorkstreamPatternEngineSource:
        """Create an instance of IdentifiedWorkstreamPatternEngineSource from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of raw
        if self.raw:
            _dict['raw'] = self.raw.to_dict()
        # override the default output from pydantic by calling `to_dict()` of created
        if self.created:
            _dict['created'] = self.created.to_dict()
        # override the default output from pydantic by calling `to_dict()` of updated
        if self.updated:
            _dict['updated'] = self.updated.to_dict()
        # override the default output from pydantic by calling `to_dict()` of score
        if self.score:
            _dict['score'] = self.score.to_dict()
        # override the default output from pydantic by calling `to_dict()` of summaries
        if self.summaries:
            _dict['summaries'] = self.summaries.to_dict()
        # override the default output from pydantic by calling `to_dict()` of workstream_events
        if self.workstream_events:
            _dict['workstream_events'] = self.workstream_events.to_dict()
        # override the default output from pydantic by calling `to_dict()` of conversations
        if self.conversations:
            _dict['conversations'] = self.conversations.to_dict()
        # override the default output from pydantic by calling `to_dict()` of accessibility
        if self.accessibility:
            _dict['accessibility'] = self.accessibility.to_dict()
        # override the default output from pydantic by calling `to_dict()` of messages
        if self.messages:
            _dict['messages'] = self.messages.to_dict()
        # override the default output from pydantic by calling `to_dict()` of websites
        if self.websites:
            _dict['websites'] = self.websites.to_dict()
        # override the default output from pydantic by calling `to_dict()` of anchors
        if self.anchors:
            _dict['anchors'] = self.anchors.to_dict()
        # override the default output from pydantic by calling `to_dict()` of persons
        if self.persons:
            _dict['persons'] = self.persons.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IdentifiedWorkstreamPatternEngineSource:
        """Create an instance of IdentifiedWorkstreamPatternEngineSource from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IdentifiedWorkstreamPatternEngineSource.parse_obj(obj)

        _obj = IdentifiedWorkstreamPatternEngineSource.parse_obj({
            "var_schema": EmbeddedModelSchema.from_dict(obj.get("schema")) if obj.get("schema") is not None else None,
            "id": obj.get("id"),
            "raw": WorkstreamPatternEngineSource.from_dict(obj.get("raw")) if obj.get("raw") is not None else None,
            "created": GroupedTimestamp.from_dict(obj.get("created")) if obj.get("created") is not None else None,
            "updated": GroupedTimestamp.from_dict(obj.get("updated")) if obj.get("updated") is not None else None,
            "filter": obj.get("filter"),
            "score": Score.from_dict(obj.get("score")) if obj.get("score") is not None else None,
            "readable": obj.get("readable"),
            "summaries": FlattenedWorkstreamSummaries.from_dict(obj.get("summaries")) if obj.get("summaries") is not None else None,
            "workstream_events": FlattenedWorkstreamEvents.from_dict(obj.get("workstream_events")) if obj.get("workstream_events") is not None else None,
            "conversations": FlattenedConversations.from_dict(obj.get("conversations")) if obj.get("conversations") is not None else None,
            "accessibility": WorkstreamPatternEngineSourceSupportedAccessibility.from_dict(obj.get("accessibility")) if obj.get("accessibility") is not None else None,
            "messages": FlattenedConversationMessages.from_dict(obj.get("messages")) if obj.get("messages") is not None else None,
            "websites": FlattenedWebsites.from_dict(obj.get("websites")) if obj.get("websites") is not None else None,
            "anchors": FlattenedAnchors.from_dict(obj.get("anchors")) if obj.get("anchors") is not None else None,
            "persons": FlattenedPersons.from_dict(obj.get("persons")) if obj.get("persons") is not None else None,
            "workstream_pattern_engine_sources_vector": obj.get("workstreamPatternEngineSourcesVector")
        })
        return _obj


