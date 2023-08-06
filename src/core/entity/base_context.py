from functools import cached_property
from redis.client import Redis

from server.python_server.src.http_server.models.api_response import ApiResponse
from src.core import Singleton, b64decode, json_loads, RedisPool


class Context(metaclass=Singleton):
    """
    App Redis Context, application service cache
    redis is necessary for auth
    """
    _redis_auth_name = "AUTH_TABLE"

    def __init__(self, **kargs):
        super().__init__()
        self.connector_auth = {}
        self.redis_conf = kargs.get("redis_conf")

    @cached_property
    def get_redis(self):
        return Redis(
            connection_pool=RedisPool(**self.redis_conf),
            decode_responses=True
        )

    def get_auth(self, carrier: str) -> dict:
        if carrier not in self.connector_auth:
            self.connector_auth[carrier] = self.get_redis_auth(carrier)
        auth = self.connector_auth.get(carrier)
        assert auth is not None, f"Auth key {carrier} no auth"
        return auth

    def get_redis_auth(self, carrier) -> dict:
        ra = self.get_redis.hget(self._redis_auth_name, carrier)
        # base64 encode
        if not ra.startswith('{'):
            ra = b64decode(ra)
        if isinstance(ra, str) and ra.startswith('{'):
            ra = json_loads(ra)
        return ra

    def set_redis_auth(self, _map: dict, auth_key: str = "") -> str:
        auth_key = auth_key or self._redis_auth_name
        ra = self.get_redis.hset(auth_key, mapping=_map)
        return str(ra)

    def reset_auth(self) -> bool:
        self.connector_auth = {}
        return True

    @cached_property
    def resp_dict(self) -> dict:
        return ApiResponse().dict()
