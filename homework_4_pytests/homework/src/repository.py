import redis

class BaseRepository:
    def cache_get(self, key):
        raise NotImplementedError

    def cache_set(self, key, score, duration):
        raise NotImplementedError



class RedisRepository(BaseRepository):
    def __init__(
        self,
        host=None,
        port=None,
        connection_timeout=None,
        operations_timeout=None,
    ):
        self.redis = redis.Redis(
            host=host,
            port=port,
            socket_connect_timeout = connection_timeout,
            socket_timeout = operations_timeout,
        )

    def cache_get(self, key):
        return self.redis.get(key)

    def cache_set(self, key, score, duration):
        if self.redis.setex(key, duration, score):
            return f'Successfully created a key {key} with value {score} and duration {duration}'