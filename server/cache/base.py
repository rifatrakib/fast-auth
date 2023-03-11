from aioredis.client import Redis


class RedisBase:
    def __init__(self, redis: Redis):
        self.redis = redis
