__all__ = ["inject_redis"]
import functools
import inspect
import logging

from typing import Awaitable, Callable
from core.redis_utils import get_redis_client

log = logging.getLogger("main")


def inject_redis[RT, **P](
    func: Callable[..., Awaitable[RT]],
) -> Callable[..., Awaitable[RT]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("function must be a coroutine")

    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        if "redis" not in kwargs.keys():
            _redis_client = get_redis_client()
            kwargs["redis"] = _redis_client
        return await func(*args, **kwargs)

    return _wrapper
