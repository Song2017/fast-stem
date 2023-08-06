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


router = APIRouter()


@router.get(
    "/health",
    responses={
        200: {"model": object, "description": "App service health status"},
    },
    tags=["health"],
    summary="health",
)
async def get_health(
) -> object:
    ...


@router.get(
    "/metrics",
    responses={
        200: {"model": str, "description": "App metrics"},
        400: {"description": "Invalid input"},
        401: {"description": "Unauthorized: provided apikey is not valid"},
        500: {"description": "Server error"},
    },
    tags=["health"],
    summary="metrics",
)
async def get_metrics(
) -> str:
    ...
