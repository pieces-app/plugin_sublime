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

from Pieces._pieces_lib.pieces_os_client.models.activities import Activities
from Pieces._pieces_lib.pieces_os_client.models.activity import Activity
from Pieces._pieces_lib.pieces_os_client.models.seeded_activity import SeededActivity
from Pieces._pieces_lib.pieces_os_client.models.streamed_identifiers import StreamedIdentifiers

from Pieces._pieces_lib.pieces_os_client.api_client import ApiClient
from Pieces._pieces_lib.pieces_os_client.api_response import ApiResponse
from Pieces._pieces_lib.pieces_os_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class ActivitiesApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def activities_create_new_activity(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, seeded_activity : Optional[SeededActivity] = None, **kwargs) -> Activity:  # noqa: E501
        """/activities/create [POST]  # noqa: E501

        This will create a new Activity.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_create_new_activity(transferables, seeded_activity, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param seeded_activity:
        :type seeded_activity: SeededActivity
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Activity
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the activities_create_new_activity_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.activities_create_new_activity_with_http_info(transferables, seeded_activity, **kwargs)  # noqa: E501

    @validate_arguments
    def activities_create_new_activity_with_http_info(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, seeded_activity : Optional[SeededActivity] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/activities/create [POST]  # noqa: E501

        This will create a new Activity.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_create_new_activity_with_http_info(transferables, seeded_activity, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param seeded_activity:
        :type seeded_activity: SeededActivity
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
        :rtype: tuple(Activity, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'transferables',
            'seeded_activity'
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
                    " to method activities_create_new_activity" % _key
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
        if _params['seeded_activity'] is not None:
            _body_params = _params['seeded_activity']

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
        _auth_settings = ['application']  # noqa: E501

        _response_types_map = {
            '200': "Activity",
            '500': "str",
        }

        return self.api_client.call_api(
            '/activities/create', 'POST',
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
    def activities_delete_specific_activity(self, activity : Annotated[StrictStr, Field(..., description="This is a specific activity uuid.")], **kwargs) -> None:  # noqa: E501
        """/activities/{activity}/delete [POST]  # noqa: E501

        This will delete a specific activity.  important note: if we delete an activity: that is going to be a generic or a specific/ we will also delete its counter part i.e the specific. and vise versa, this ensures that the references are always cleaned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_delete_specific_activity(activity, async_req=True)
        >>> result = thread.get()

        :param activity: This is a specific activity uuid. (required)
        :type activity: str
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
            message = "Error! Please call the activities_delete_specific_activity_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.activities_delete_specific_activity_with_http_info(activity, **kwargs)  # noqa: E501

    @validate_arguments
    def activities_delete_specific_activity_with_http_info(self, activity : Annotated[StrictStr, Field(..., description="This is a specific activity uuid.")], **kwargs) -> ApiResponse:  # noqa: E501
        """/activities/{activity}/delete [POST]  # noqa: E501

        This will delete a specific activity.  important note: if we delete an activity: that is going to be a generic or a specific/ we will also delete its counter part i.e the specific. and vise versa, this ensures that the references are always cleaned.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_delete_specific_activity_with_http_info(activity, async_req=True)
        >>> result = thread.get()

        :param activity: This is a specific activity uuid. (required)
        :type activity: str
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
            'activity'
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
                    " to method activities_delete_specific_activity" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['activity'] is not None:
            _path_params['activity'] = _params['activity']


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
        _auth_settings = ['application']  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            '/activities/{activity}/delete', 'POST',
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
    def activities_snapshot(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, pseudo : Annotated[Optional[StrictBool], Field(description="This is helper boolean that will give you the ability to also include your pseudo assets, we will always default to false.")] = None, **kwargs) -> Activities:  # noqa: E501
        """/activities [GET]  # noqa: E501

        This will get a snapshot of all of the activities  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_snapshot(transferables, pseudo, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param pseudo: This is helper boolean that will give you the ability to also include your pseudo assets, we will always default to false.
        :type pseudo: bool
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Activities
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the activities_snapshot_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.activities_snapshot_with_http_info(transferables, pseudo, **kwargs)  # noqa: E501

    @validate_arguments
    def activities_snapshot_with_http_info(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, pseudo : Annotated[Optional[StrictBool], Field(description="This is helper boolean that will give you the ability to also include your pseudo assets, we will always default to false.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/activities [GET]  # noqa: E501

        This will get a snapshot of all of the activities  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_snapshot_with_http_info(transferables, pseudo, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param pseudo: This is helper boolean that will give you the ability to also include your pseudo assets, we will always default to false.
        :type pseudo: bool
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
        :rtype: tuple(Activities, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'transferables',
            'pseudo'
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
                    " to method activities_snapshot" % _key
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

        if _params.get('pseudo') is not None:  # noqa: E501
            _query_params.append(('pseudo', _params['pseudo']))

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
        _auth_settings = ['application']  # noqa: E501

        _response_types_map = {
            '200': "Activities",
            '500': "str",
        }

        return self.api_client.call_api(
            '/activities', 'GET',
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
    def activities_stream_identifiers(self, **kwargs) -> StreamedIdentifiers:  # noqa: E501
        """/activities/stream/identifiers [WS]  # noqa: E501

        Provides a WebSocket connection that emits changes to your activity identifiers (UUIDs).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_stream_identifiers(async_req=True)
        >>> result = thread.get()

        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: StreamedIdentifiers
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the activities_stream_identifiers_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.activities_stream_identifiers_with_http_info(**kwargs)  # noqa: E501

    @validate_arguments
    def activities_stream_identifiers_with_http_info(self, **kwargs) -> ApiResponse:  # noqa: E501
        """/activities/stream/identifiers [WS]  # noqa: E501

        Provides a WebSocket connection that emits changes to your activity identifiers (UUIDs).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activities_stream_identifiers_with_http_info(async_req=True)
        >>> result = thread.get()

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
        :rtype: tuple(StreamedIdentifiers, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
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
                    " to method activities_stream_identifiers" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

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
            ['application/json', 'text/plain'])  # noqa: E501

        # authentication setting
        _auth_settings = ['application']  # noqa: E501

        _response_types_map = {
            '200': "StreamedIdentifiers",
            '500': "str",
        }

        return self.api_client.call_api(
            '/activities/stream/identifiers', 'GET',
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
