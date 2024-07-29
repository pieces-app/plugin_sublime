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
from Pieces._pieces_lib.pydantic import Field, StrictBool

from typing import Optional

from Pieces._pieces_lib.pieces_os_client.models.discovered_assets import DiscoveredAssets
from Pieces._pieces_lib.pieces_os_client.models.discovered_html_webpages import DiscoveredHtmlWebpages
from Pieces._pieces_lib.pieces_os_client.models.discovered_related_tags import DiscoveredRelatedTags
from Pieces._pieces_lib.pieces_os_client.models.discovered_sensitives import DiscoveredSensitives
from Pieces._pieces_lib.pieces_os_client.models.seeded_discoverable_assets import SeededDiscoverableAssets
from Pieces._pieces_lib.pieces_os_client.models.seeded_discoverable_html_webpages import SeededDiscoverableHtmlWebpages
from Pieces._pieces_lib.pieces_os_client.models.seeded_discoverable_related_tags import SeededDiscoverableRelatedTags
from Pieces._pieces_lib.pieces_os_client.models.seeded_discoverable_sensitives import SeededDiscoverableSensitives

from Pieces._pieces_lib.pieces_os_client.api_client import ApiClient
from Pieces._pieces_lib.pieces_os_client.api_response import ApiResponse
from Pieces._pieces_lib.pieces_os_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class DiscoveryApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def discovery_discover_assets(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_assets : Annotated[Optional[SeededDiscoverableAssets], Field(description="The discovery/discover/assets endpoint will accept seededDiscoverableAssets, that represetns an iterable of multiple fragments or files.")] = None, **kwargs) -> DiscoveredAssets:  # noqa: E501
        """/discovery/discover/assets [POST]  # noqa: E501

        This is the endpoint used for bulk import. In both cases of the bulk import flow, fragments or files. When we already have \"snippets\" or fragments to discover and now our job is to check if they are actually valid snippets(clustering). Otherwise, we should have a file to parse && snippitize and then run through the clustering.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_assets(automatic, seeded_discoverable_assets, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_assets: The discovery/discover/assets endpoint will accept seededDiscoverableAssets, that represetns an iterable of multiple fragments or files.
        :type seeded_discoverable_assets: SeededDiscoverableAssets
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DiscoveredAssets
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the discovery_discover_assets_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.discovery_discover_assets_with_http_info(automatic, seeded_discoverable_assets, **kwargs)  # noqa: E501

    @validate_arguments
    def discovery_discover_assets_with_http_info(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_assets : Annotated[Optional[SeededDiscoverableAssets], Field(description="The discovery/discover/assets endpoint will accept seededDiscoverableAssets, that represetns an iterable of multiple fragments or files.")] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/discovery/discover/assets [POST]  # noqa: E501

        This is the endpoint used for bulk import. In both cases of the bulk import flow, fragments or files. When we already have \"snippets\" or fragments to discover and now our job is to check if they are actually valid snippets(clustering). Otherwise, we should have a file to parse && snippitize and then run through the clustering.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_assets_with_http_info(automatic, seeded_discoverable_assets, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_assets: The discovery/discover/assets endpoint will accept seededDiscoverableAssets, that represetns an iterable of multiple fragments or files.
        :type seeded_discoverable_assets: SeededDiscoverableAssets
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
        :rtype: tuple(DiscoveredAssets, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'automatic',
            'seeded_discoverable_assets'
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
                    " to method discovery_discover_assets" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('automatic') is not None:  # noqa: E501
            _query_params.append(('automatic', _params['automatic']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['seeded_discoverable_assets'] is not None:
            _body_params = _params['seeded_discoverable_assets']

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
            '200': "DiscoveredAssets",
            '500': "str",
        }

        return self.api_client.call_api(
            '/discovery/discover/assets', 'POST',
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
    def discovery_discover_assets_html(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_html_webpages : Optional[SeededDiscoverableHtmlWebpages] = None, **kwargs) -> DiscoveredHtmlWebpages:  # noqa: E501
        """/discovery/discover/assets/html[POST]  # noqa: E501

        This is the discover discover assets html endpoint. The goal of this endpoint is to either take an iterable of urls and pages(an html string) and extract all the assets from the iterable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_assets_html(automatic, seeded_discoverable_html_webpages, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_html_webpages:
        :type seeded_discoverable_html_webpages: SeededDiscoverableHtmlWebpages
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DiscoveredHtmlWebpages
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the discovery_discover_assets_html_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.discovery_discover_assets_html_with_http_info(automatic, seeded_discoverable_html_webpages, **kwargs)  # noqa: E501

    @validate_arguments
    def discovery_discover_assets_html_with_http_info(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_html_webpages : Optional[SeededDiscoverableHtmlWebpages] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/discovery/discover/assets/html[POST]  # noqa: E501

        This is the discover discover assets html endpoint. The goal of this endpoint is to either take an iterable of urls and pages(an html string) and extract all the assets from the iterable.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_assets_html_with_http_info(automatic, seeded_discoverable_html_webpages, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_html_webpages:
        :type seeded_discoverable_html_webpages: SeededDiscoverableHtmlWebpages
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
        :rtype: tuple(DiscoveredHtmlWebpages, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'automatic',
            'seeded_discoverable_html_webpages'
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
                    " to method discovery_discover_assets_html" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('automatic') is not None:  # noqa: E501
            _query_params.append(('automatic', _params['automatic']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['seeded_discoverable_html_webpages'] is not None:
            _body_params = _params['seeded_discoverable_html_webpages']

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
            '200': "DiscoveredHtmlWebpages",
            '500': "str",
        }

        return self.api_client.call_api(
            '/discovery/discover/assets/html', 'POST',
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
    def discovery_discover_sensitives(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_sensitives : Optional[SeededDiscoverableSensitives] = None, **kwargs) -> DiscoveredSensitives:  # noqa: E501
        """/discovery/discover/sensitives [POST]  # noqa: E501

        This endpoint will accept an array of text values, and attampt to extract sensitive data out of it.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_sensitives(automatic, seeded_discoverable_sensitives, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_sensitives:
        :type seeded_discoverable_sensitives: SeededDiscoverableSensitives
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DiscoveredSensitives
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the discovery_discover_sensitives_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.discovery_discover_sensitives_with_http_info(automatic, seeded_discoverable_sensitives, **kwargs)  # noqa: E501

    @validate_arguments
    def discovery_discover_sensitives_with_http_info(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_sensitives : Optional[SeededDiscoverableSensitives] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/discovery/discover/sensitives [POST]  # noqa: E501

        This endpoint will accept an array of text values, and attampt to extract sensitive data out of it.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_sensitives_with_http_info(automatic, seeded_discoverable_sensitives, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_sensitives:
        :type seeded_discoverable_sensitives: SeededDiscoverableSensitives
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
        :rtype: tuple(DiscoveredSensitives, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'automatic',
            'seeded_discoverable_sensitives'
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
                    " to method discovery_discover_sensitives" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('automatic') is not None:  # noqa: E501
            _query_params.append(('automatic', _params['automatic']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['seeded_discoverable_sensitives'] is not None:
            _body_params = _params['seeded_discoverable_sensitives']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = []  # noqa: E501

        _response_types_map = {
            '200': "DiscoveredSensitives",
        }

        return self.api_client.call_api(
            '/discovery/discover/sensitives', 'POST',
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
    def discovery_discover_tags_related(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_related_tags : Optional[SeededDiscoverableRelatedTags] = None, **kwargs) -> DiscoveredRelatedTags:  # noqa: E501
        """/discovery/discover/tags/related [POST]  # noqa: E501

        This will take in a tag or multiple tags and return all the tags that are related to the tag or tag provide in the body.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_tags_related(automatic, seeded_discoverable_related_tags, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_related_tags:
        :type seeded_discoverable_related_tags: SeededDiscoverableRelatedTags
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _request_timeout: timeout setting for this request.
               If one number provided, it will be total request
               timeout. It can also be a pair (tuple) of
               (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: DiscoveredRelatedTags
        """
        kwargs['_return_http_data_only'] = True
        if '_preload_content' in kwargs:
            message = "Error! Please call the discovery_discover_tags_related_with_http_info method with `_preload_content` instead and obtain raw data from ApiResponse.raw_data"  # noqa: E501
            raise ValueError(message)
        return self.discovery_discover_tags_related_with_http_info(automatic, seeded_discoverable_related_tags, **kwargs)  # noqa: E501

    @validate_arguments
    def discovery_discover_tags_related_with_http_info(self, automatic : Annotated[Optional[StrictBool], Field(description="For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.")] = None, seeded_discoverable_related_tags : Optional[SeededDiscoverableRelatedTags] = None, **kwargs) -> ApiResponse:  # noqa: E501
        """/discovery/discover/tags/related [POST]  # noqa: E501

        This will take in a tag or multiple tags and return all the tags that are related to the tag or tag provide in the body.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.discovery_discover_tags_related_with_http_info(automatic, seeded_discoverable_related_tags, async_req=True)
        >>> result = thread.get()

        :param automatic: For most cases set to true. If this is set to true we will handle the behavior automically or else we will not proactively handle specific behavior but we will let the developer decide the behavior.
        :type automatic: bool
        :param seeded_discoverable_related_tags:
        :type seeded_discoverable_related_tags: SeededDiscoverableRelatedTags
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
        :rtype: tuple(DiscoveredRelatedTags, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'automatic',
            'seeded_discoverable_related_tags'
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
                    " to method discovery_discover_tags_related" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []
        if _params.get('automatic') is not None:  # noqa: E501
            _query_params.append(('automatic', _params['automatic']))

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        if _params['seeded_discoverable_related_tags'] is not None:
            _body_params = _params['seeded_discoverable_related_tags']

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
            '200': "DiscoveredRelatedTags",
            '500': "str",
        }

        return self.api_client.call_api(
            '/discovery/discover/tags/related', 'POST',
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
