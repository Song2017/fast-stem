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

from server.python_server.src.http_server.models.api_response import ApiResponse
from server.python_server.src.http_server.models.extra_models import TokenModel
from src.api.security_api import get_token_ca_key
from src.service.biz.user.user_context import UserContext
from src.service.biz.user.user_mapping import UserMapping

router = APIRouter()
_user_context = UserContext()


@router.get(
    "/id_check",
    responses={
        200: {"model": ApiResponse,
              "description": "User ID and Name has been checked successfully."},
        400: {"description": "Invalid input."},
        404: {"description": "id check failed."},
        500: {"model": ApiResponse, "description": "id retrieval failed."},
    },
    tags=["user"],
    summary="idCheck",
)
async def id_check(
        user_id: str = Query(None, description="Customer ID"),
        name: str = Query(None, description="Customer Name"),
        cache: str = Query(
            None, description="Cache that customer ID and name is matched. "
                              "If the value is disable, the cache will not be checked"),
        _: TokenModel = Security(
            get_token_ca_key
        ),
) -> ApiResponse:
    """Check if the user is valid."""
    data = await UserMapping(context=_user_context)(
        user_id=user_id, name=name, cache=cache)
    return ApiResponse(**data)
