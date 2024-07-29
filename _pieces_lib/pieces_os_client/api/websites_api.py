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

from Pieces._pieces_lib.pieces_os_client.models.existent_metadata import ExistentMetadata
from Pieces._pieces_lib.pieces_os_client.models.existing_metadata import ExistingMetadata
from Pieces._pieces_lib.pieces_os_client.models.search_input import SearchInput
from Pieces._pieces_lib.pieces_os_client.models.searched_websites import SearchedWebsites
from Pieces._pieces_lib.pieces_os_client.models.seeded_website import SeededWebsite
from Pieces._pieces_lib.pieces_os_client.models.website import Website
from Pieces._pieces_lib.pieces_os_client.models.websites import Websites

from Pieces._pieces_lib.pieces_os_client.api_client import ApiClient
from Pieces._pieces_lib.pieces_os_client.api_response import ApiResponse
from Pieces._pieces_lib.pieces_os_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class WebsitesApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def search_websites(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, search_input : Optional[SearchInput] = None, **kwargs) -> SearchedWebsites:  # noqa: E501
        """/websites/search [POST]  # noqa: E501

        This will search your websites for a specific website  note: we will search the url, and search the name of the website  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.search_websites(transferables, search_input, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param search_input:
        :type search_input: SearchInput
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: SearchedWebsites
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the search_websites_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.search_websites_with_http_info(transferables, search_input, **kwargs)  # noqa: E501

    @validate_arguments
    def search_websites_with_http_info(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, search_input : Optional[SearchInput] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/websites/search [POST]  # noqa: E501

        This will search your websites for a specific website  note: we will search the url, and search the name of the website  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.search_websites_with_http_info(transferables, search_input, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param search_input:
        :type search_input: SearchInput
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
        :rtype: tuple(SearchedWebsites, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'transferables',
            'search_input'
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
                    " to method search_websites" % _key
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
        if _params['search_input'] is not None:
            _body_params = _params['search_input']

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
            '200': "SearchedWebsites",
            '500': "str",
        }

        return self.api_client.call_api(
            '/websites/search', 'POST',
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
    def websites_create_new_website(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, seeded_website : Optional[SeededWebsite] = None, **kwargs) -> Website:  # noqa: E501
        """/websites/create [POST]  # noqa: E501

        This will create a website and attach it to a specific asset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_create_new_website(transferables, seeded_website, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param seeded_website:
        :type seeded_website: SeededWebsite
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: Website
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the websites_create_new_website_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.websites_create_new_website_with_http_info(transferables, seeded_website, **kwargs)  # noqa: E501

    @validate_arguments
    def websites_create_new_website_with_http_info(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, seeded_website : Optional[SeededWebsite] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/websites/create [POST]  # noqa: E501

        This will create a website and attach it to a specific asset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_create_new_website_with_http_info(transferables, seeded_website, async_req=True)
        >>> result = thread.get()

        :param transferables: This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)
        :type transferables: bool
        :param seeded_website:
        :type seeded_website: SeededWebsite
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
        :rtype: tuple(Website, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'transferables',
            'seeded_website'
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
                    " to method websites_create_new_website" % _key
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
        if _params['seeded_website'] is not None:
            _body_params = _params['seeded_website']

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
            '200': "Website",
            '500': "str",
        }

        return self.api_client.call_api(
            '/websites/create', 'POST',
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
    def websites_delete_specific_website(self, website : Annotated[StrictStr, Field(..., description="website id")], **kwargs) -> None:  # noqa: E501
        """/websites/{website}/delete [POST]  # noqa: E501

        This will delete a specific website!  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_delete_specific_website(website, async_req=True)
        >>> result = thread.get()

        :param website: website id (required)
        :type website: str
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
            message = "Error! Please call the websites_delete_specific_website_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.websites_delete_specific_website_with_http_info(website, **kwargs)  # noqa: E501

    @validate_arguments
    def websites_delete_specific_website_with_http_info(self, website : Annotated[StrictStr, Field(..., description="website id")], **kwargs) -> ApiResponse:  # noqa: E501
        """/websites/{website}/delete [POST]  # noqa: E501

        This will delete a specific website!  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_delete_specific_website_with_http_info(website, async_req=True)
        >>> result = thread.get()

        :param website: website id (required)
        :type website: str
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
            'website'
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
                    " to method websites_delete_specific_website" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params['website'] is not None:
            _path_params['website'] = _params['website']


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
            '/websites/{website}/delete', 'POST',
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
    def websites_exists(self, existent_metadata : Optional[ExistentMetadata] = None, **kwargs) -> ExistingMetadata:  # noqa: E501
        """/websites/exists [POST]  # noqa: E501

        This will check all of the websites in our database to see if this specific provided website actually exists, if not we will just return a null website in the output.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_exists(existent_metadata, async_req=True)
        >>> result = thread.get()

        :param existent_metadata:
        :type existent_metadata: ExistentMetadata
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ExistingMetadata
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the websites_exists_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.websites_exists_with_http_info(existent_metadata, **kwargs)  # noqa: E501

    @validate_arguments
    def websites_exists_with_http_info(self, existent_metadata : Optional[ExistentMetadata] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/websites/exists [POST]  # noqa: E501

        This will check all of the websites in our database to see if this specific provided website actually exists, if not we will just return a null website in the output.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_exists_with_http_info(existent_metadata, async_req=True)
        >>> result = thread.get()

        :param existent_metadata:
        :type existent_metadata: ExistentMetadata
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
        :rtype: tuple(ExistingMetadata, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'existent_metadata'
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
                    " to method websites_exists" % _key
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
        if _params['existent_metadata'] is not None:
            _body_params = _params['existent_metadata']

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
            '200': "ExistingMetadata",
            '500': "str",
        }

        return self.api_client.call_api(
            '/websites/exists', 'POST',
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
    def websites_snapshot(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, **kwargs) -> Websites:  # noqa: E501
        """/websites [GET]  # noqa: E501

        This will get a snapshot of all your websites.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_snapshot(transferables, async_req=True)
        >>> result = thread.get()

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
        :rtype: Websites
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the websites_snapshot_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.websites_snapshot_with_http_info(transferables, **kwargs)  # noqa: E501

    @validate_arguments
    def websites_snapshot_with_http_info(self, transferables : Annotated[Optional[StrictBool], Field(description="This is a boolean that will decided if we are want to return the transferable data (default) or not(performance enhancement)")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/websites [GET]  # noqa: E501

        This will get a snapshot of all your websites.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.websites_snapshot_with_http_info(transferables, async_req=True)
        >>> result = thread.get()

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
        :rtype: tuple(Websites, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
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
                    " to method websites_snapshot" % _key
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
        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain'])  # noqa: E501

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "Websites",
            '500': "str",
        }

        return self.api_client.call_api(
            '/websites', 'GET',
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
