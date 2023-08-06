# coding: utf-8

from typing import Dict, List  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from http_server.models.extra_models import TokenModel  # noqa: F401
from http_server.models.api_response import ApiResponse
from http_server.security_api import get_token_ca_key

router = APIRouter()


@router.get(
    "/config/connector/{id}",
    responses={
        200: {"model": ApiResponse, "description": "User ID and Name has been checked successfully."},
        400: {"description": "Invalid input."},
        404: {"description": "id check failed."},
        500: {"model": ApiResponse, "description": "id retrieval failed."},
    },
    tags=["config"],
    summary="GetConfig",
)
async def get_config(
    id: str = Path(None, description="Connector Id, e.g. sfexpress.test"),
    connector: str = Query(None, description="Connector-self Name"),
    cache: str = Query(None, description="Cache that customer ID and name is matched. If the value is &#x60;disable&#x60;, the cache will not be checked"),
    token_ca_key: TokenModel = Security(
        get_token_ca_key
    ),
) -> ApiResponse:
    """Get connector config."""
    ...
