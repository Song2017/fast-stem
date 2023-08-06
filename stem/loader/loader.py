import copy


class Loader:
    """
    Loader
    receive requests from server
    """
    HANDLER_KEY: str = ""
    _handler_map = dict()

    def __init__(self, handler, connector=None):
        self.connector = connector
        self.handler_cls = handler
        # https://stackoverflow.com/questions/35569042/ssl-certificate-verify-failed-with-python3  # noqa:E501
        # ssl._create_default_https_context = ssl._create_unverified_context

    async def __call__(self, *args, **kw):
        req_params: dict = await self.req_params(args, kw)
        if not self.HANDLER_KEY:
            handler = self.handler_cls()
        elif self.HANDLER_KEY in self._handler_map:
            handler = self._handler_map[self.HANDLER_KEY]
        else:
            self._handler_map[self.HANDLER_KEY] = self.handler_cls()
            handler = self._handler_map[self.HANDLER_KEY]

        instance = await handler(**req_params)
        return instance

    async def req_params(self, args: tuple, kw: dict):
        params: dict = copy.deepcopy(kw)
        params.update({"args": args})
        req_params = {
            "original_params": {
                "input_args": args,
                "input_kw": kw,
            },

            "_input": params,
            "_body": kw.get("body"),
            "connector": self.connector,
        }
        return req_params
