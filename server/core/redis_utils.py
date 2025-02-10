from typing import AsyncGenerator

import redis.asyncio as aioredis

from config import settings


async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    """
    Returns a Redis client session from the connection pool.
    Ensures proper cleanup by closing the client after use.
    """
    # Create a Redis client from the connection pool
    client: aioredis.Redis = aioredis.from_url(str(settings.redis_dsn))  # type: ignore
    try:
        yield client
    finally:
        # Ensure the client is properly closed
        await client.aclose()
