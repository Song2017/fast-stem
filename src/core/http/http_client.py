import httpx
from httpx import Response

from src.core.log.decorator import req_log

HTTP_TIMEOUT = 15.0
HTTP_VERIFY = False


@req_log()
async def call_http(url: str, **kwargs) -> tuple:
    http_func = kwargs.pop("http_func", "post")
    verify = kwargs.pop("verify", HTTP_VERIFY)
    timeout = kwargs.pop("timeout", HTTP_TIMEOUT)
    async with httpx.AsyncClient(
            verify=verify, timeout=timeout) as client:
        func = getattr(client, http_func)
        # client.post()
        rsp: Response = await func(
            url,
            **kwargs,
        )
    return rsp.status_code, rsp


@req_log()
def call_http_sync(url: str, **kwargs) -> tuple:
    http_func = kwargs.pop("http_func", "post")
    verify = kwargs.pop("verify", HTTP_VERIFY)
    timeout = kwargs.pop("timeout", HTTP_TIMEOUT)
    with httpx.Client(
            verify=verify, timeout=timeout) as client:
        func = getattr(client, http_func)
        # client.post()
        rsp: Response = func(
            url,
            **kwargs,
        )
    return rsp.status_code, rsp
