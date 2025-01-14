import functools
import inspect
from typing import  Awaitable, Callable,cast

from sqlalchemy.ext.asyncio import AsyncSession

from database.session_manager import get_async_session
from .redis_utils import get_redis_client


def inject_redis[RT, **P](func: Callable[..., Awaitable[RT]]) -> Callable[...,Awaitable[RT]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("function must be a coroutine")
    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        if 'redis' not in kwargs.keys():
            _redis_client = get_redis_client()
            kwargs['redis'] = _redis_client
        return await func(*args, **kwargs)
    return _wrapper


def inject_asyncpg_session[RT, **P](func: Callable[..., Awaitable[RT]]) -> Callable[...,Awaitable[RT]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("function must be a coroutine")
    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        if 'session' not in kwargs.keys():
            async with get_async_session() as session:
                kwargs['session'] = session
                return await func(*args, **kwargs)
        elif isinstance(kwargs['session'], ...):
                with get_async_session() as session:
                    kwargs['session'] = session
                    return await func(*args, **kwargs)

        elif not isinstance(kwargs['session'], AsyncSession):
            raise TypeError("session must be an AsyncSession")

    return cast(Callable[..., Awaitable[RT]],_wrapper)
