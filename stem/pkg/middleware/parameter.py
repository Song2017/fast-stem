from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send
from urllib.parse import parse_qs


class ParameterMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if "order" in scope["path"]:
            query_string = (scope.get("query_string") or b"").decode()
            query_dict = parse_qs(query_string)
            store = query_dict.get("store")
            if store and '.' not in store[0]:
                await self.preflight_response({
                    "message": "Parameter store format should be [platform.storeName]",
                })(scope, receive, send)
                return
        await self.app(scope, receive, send)

    @staticmethod
    def preflight_response(resp: dict) -> Response:
        return JSONResponse(resp, status_code=400)
