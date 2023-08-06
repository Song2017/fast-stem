from redis.connection import BlockingConnectionPool


class RedisPool(BlockingConnectionPool):
    def __init__(self, **kwargs):
        redis_conf = kwargs
        _kwargs = {
            "max_connections": 10,
            "timeout": 10,
            "host": redis_conf.pop("redis_server", ""),
            "password": redis_conf.pop("redis_password", ""),
            "socket_timeout": 5,  # seconds
            "decode_responses": True,
        }
        _kwargs.update(redis_conf)
        super(RedisPool, self).__init__(**_kwargs)
