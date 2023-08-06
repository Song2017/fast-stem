# coding: utf-8
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from server.python_server.src.http_server.models.extra_models import TokenModel
from stem.pkg import APP_CONF


def get_token_ca_key(
        token_api_key_header: str = Security(
            APIKeyHeader(name="Authorization", auto_error=False)
        ),
) -> TokenModel:
    """
    Check and retrieve authentication information from api_key.

    :param token_api_key_header API key provided by Authorization[x-ca-key] header

    :type token_api_key_header: str
    :return: Information attached to provided api_key or None 
    if api_key is invalid or does not allow access to called API
    :rtype: TokenModel | None
    """  # noqa:E501
    if token_api_key_header == APP_CONF.SECURITY_KEY:
        return TokenModel(sub="")
    else:
        raise HTTPException(
            status_code=401, detail="The API key is required"
        )


def get_token_ca_stage(
        token_api_key_header: str = Security(
            APIKeyHeader(name="x-ca-stage", auto_error=False)
        ),
) -> TokenModel:
    """
    Check and retrieve authentication information from api_key.

    :param token_api_key_header API key provided by Authorization[x-ca-stage] header


    :type token_api_key_header: str
    :return: Information attached to provided api_key or None 
    if api_key is invalid or does not allow access to called API
    :rtype: TokenModel | None
    """  # noqa:E501

    ...
