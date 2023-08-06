from starlette.types import ASGIApp, Receive, Scope, Send


class AuthMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if "cbec" in scope["path"]:
            scope["headers"].append(("conf", b'{}'))
            await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)
