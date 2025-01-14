import redis.asyncio as aioredis

from config import settings


def get_redis_client() -> aioredis.Redis:
    """
    returns redis client session from pool
    """
    return aioredis.from_url(settings.redis_dsn)
