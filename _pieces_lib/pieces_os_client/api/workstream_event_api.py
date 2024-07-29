# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import re  # noqa: F401
import io
import warnings

from Pieces._pieces_lib.pydantic import validate_arguments, ValidationError

from Pieces._pieces_lib.typing_extensions import Annotated
from Pieces._pieces_lib.pydantic import Field, StrictBool, StrictStr

from typing import Optional

from Pieces._pieces_lib.pieces_os_client.models.seeded_score_increment import SeededScoreIncrement
from Pieces._pieces_lib.pieces_os_client.models.workstream_event import WorkstreamEvent

from Pieces._pieces_lib.pieces_os_client.api_client import ApiClient
from Pieces._pieces_lib.pieces_os_client.api_response import ApiResponse
from Pieces._pieces_lib.pieces_os_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class WorkstreamEventApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def workstream_event_associate_workstream_summary(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], workstream_summary : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_summary.")], **kwargs) -> None:  # noqa: E501
        """/workstream_event/{workstream_event}/workstream_summaries/associate/{workstream_summary} [POST]  # noqa: E501

        This will associate a workstream_event with a workstream summary. This will do the same thing as the workstreamSummary equivalent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_associate_workstream_summary(workstream_event, workstream_summary, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param workstream_summary: This is a identifier that is used to identify a specific workstream_summary. (required)
        :type workstream_summary: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the workstream_event_associate_workstream_summary_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.workstream_event_associate_workstream_summary_with_http_info(workstream_event, workstream_summary, **kwargs)  # noqa: E501

    @validate_arguments
    def workstream_event_associate_workstream_summary_with_http_info(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], workstream_summary : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_summary.")], **kwargs) -> ApiResponse:  # noqa: E501
        """/workstream_event/{workstream_event}/workstream_summaries/associate/{workstream_summary} [POST]  # noqa: E501

        This will associate a workstream_event with a workstream summary. This will do the same thing as the workstreamSummary equivalent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_associate_workstream_summary_with_http_info(workstream_event, workstream_summary, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param workstream_summary: This is a identifier that is used to identify a specific workstream_summary. (required)
        :type workstream_summary: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        _params = locals()

        _all_params = [
            'workstream_event',
            'workstream_summary'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workstream_event_associate_workstream_summary" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['workstream_event'] is not None:
            _path_params['workstream_event'] = _params['workstream_event']

        if _params['workstream_summary'] is not None:
            _path_params['workstream_summary'] = _params['workstream_summary']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            '/workstream_event/{workstream_event}/workstream_summaries/associate/{workstream_summary}', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def workstream_event_disassociate_workstream_summary(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], workstream_summary : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_summary.")], **kwargs) -> None:  # noqa: E501
        """/workstream_event/{workstream_event}/workstream_summaries/disassociate/{workstream_summary} [POST]  # noqa: E501

        This will enable us to disassociate a workstream_event from a workstream summary. This will do the same thing as the workstreamSummary equivalent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_disassociate_workstream_summary(workstream_event, workstream_summary, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param workstream_summary: This is a identifier that is used to identify a specific workstream_summary. (required)
        :type workstream_summary: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the workstream_event_disassociate_workstream_summary_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.workstream_event_disassociate_workstream_summary_with_http_info(workstream_event, workstream_summary, **kwargs)  # noqa: E501

    @validate_arguments
    def workstream_event_disassociate_workstream_summary_with_http_info(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], workstream_summary : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_summary.")], **kwargs) -> ApiResponse:  # noqa: E501
        """/workstream_event/{workstream_event}/workstream_summaries/disassociate/{workstream_summary} [POST]  # noqa: E501

        This will enable us to disassociate a workstream_event from a workstream summary. This will do the same thing as the workstreamSummary equivalent.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_disassociate_workstream_summary_with_http_info(workstream_event, workstream_summary, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param workstream_summary: This is a identifier that is used to identify a specific workstream_summary. (required)
        :type workstream_summary: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        _params = locals()

        _all_params = [
            'workstream_event',
            'workstream_summary'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workstream_event_disassociate_workstream_summary" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['workstream_event'] is not None:
            _path_params['workstream_event'] = _params['workstream_event']

        if _params['workstream_summary'] is not None:
            _path_params['workstream_summary'] = _params['workstream_summary']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            '/workstream_event/{workstream_event}/workstream_summaries/disassociate/{workstream_summary}', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def workstream_event_scores_increment(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], seeded_score_increment : Optional[SeededScoreIncrement] = None, **kwargs) -> None:  # noqa: E501
        """'/workstream_event/{workstream_event}/scores/increment' [POST]  # noqa: E501

        This will take in a SeededScoreIncrement and will increment the material relative to the incoming body.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_scores_increment(workstream_event, seeded_score_increment, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param seeded_score_increment:
        :type seeded_score_increment: SeededScoreIncrement
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the workstream_event_scores_increment_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.workstream_event_scores_increment_with_http_info(workstream_event, seeded_score_increment, **kwargs)  # noqa: E501

    @validate_arguments
    def workstream_event_scores_increment_with_http_info(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], seeded_score_increment : Optional[SeededScoreIncrement] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """'/workstream_event/{workstream_event}/scores/increment' [POST]  # noqa: E501

        This will take in a SeededScoreIncrement and will increment the material relative to the incoming body.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_scores_increment_with_http_info(workstream_event, seeded_score_increment, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param seeded_score_increment:
        :type seeded_score_increment: SeededScoreIncrement
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        _params = locals()

        _all_params = [
            'workstream_event',
            'seeded_score_increment'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workstream_event_scores_increment" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['workstream_event'] is not None:
            _path_params['workstream_event'] = _params['workstream_event']


        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['seeded_score_increment'] is not None:
            _body_params = _params['seeded_score_increment']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            '/workstream_event/{workstream_event}/scores/increment', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def workstream_event_update(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, workstream_event : Optional[WorkstreamEvent] = None, **kwargs) -> WorkstreamEvent:  # noqa: E501
        """/workstream_event/update [POST]  # noqa: E501

        This will update a specific workstream_event.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_update(transferables, workstream_event, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param workstream_event:
        :type workstream_event: WorkstreamEvent
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: WorkstreamEvent
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the workstream_event_update_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.workstream_event_update_with_http_info(transferables, workstream_event, **kwargs)  # noqa: E501

    @validate_arguments
    def workstream_event_update_with_http_info(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, workstream_event : Optional[WorkstreamEvent] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/workstream_event/update [POST]  # noqa: E501

        This will update a specific workstream_event.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_event_update_with_http_info(transferables, workstream_event, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param workstream_event:
        :type workstream_event: WorkstreamEvent
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(WorkstreamEvent, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'transferables',
            'workstream_event'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workstream_event_update" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('transferables') is not None:  # noqa: E501
            _query_params.append(('transferables', _params['transferables']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['workstream_event'] is not None:
            _body_params = _params['workstream_event']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "WorkstreamEvent",
            '500': "str",
        }

        return self.api_client.call_api(
            '/workstream_event/update', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def workstream_events_specific_workstream_event_snapshot(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, **kwargs) -> WorkstreamEvent:  # noqa: E501
        """/workstream_event/{workstream_event} [GET]  # noqa: E501

        This will get a snapshot of a single workstream_event.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_events_specific_workstream_event_snapshot(workstream_event, transferables, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: WorkstreamEvent
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the workstream_events_specific_workstream_event_snapshot_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.workstream_events_specific_workstream_event_snapshot_with_http_info(workstream_event, transferables, **kwargs)  # noqa: E501

    @validate_arguments
    def workstream_events_specific_workstream_event_snapshot_with_http_info(self, workstream_event : Annotated[StrictStr, Field(..., description="This is a identifier that is used to identify a specific workstream_event.")], transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/workstream_event/{workstream_event} [GET]  # noqa: E501

        This will get a snapshot of a single workstream_event.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.workstream_events_specific_workstream_event_snapshot_with_http_info(workstream_event, transferables, async_req=True)
        >>> result = thread.get()

        :param workstream_event: This is a identifier that is used to identify a specific workstream_event. (required)
        :type workstream_event: str
        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the ApiResponse.data will
                                 be set to none and raw_data will store the
                                 HTTP response body without reading/decoding.
                                 Default is True.
        :type _preload_content: bool, optional
        :param _return_http_data_only: response data instead of ApiResponse
                                       object with status code, headers, etc
        :type _return_http_data_only: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(WorkstreamEvent, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'workstream_event',
            'transferables'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method workstream_events_specific_workstream_event_snapshot" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['workstream_event'] is not None:
            _path_params['workstream_event'] = _params['workstream_event']


        # process the query parameters
        _query_params = []
        if _params.get('transferables') is not None:  # noqa: E501
            _query_params.append(('transferables', _params['transferables']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "WorkstreamEvent",
            '410': "str",
        }

        return self.api_client.call_api(
            '/workstream_event/{workstream_event}', 'GET',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
