from src.core import BaseMapping


class UserMapping(BaseMapping):
    async def rpc(self, **kwargs) -> dict:
        """
        consume 3rd-provider service and format for deserialize
        """
        print(kwargs)
        return dict()
