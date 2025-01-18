import functools
import inspect
import logging
from typing import Awaitable, Callable, cast

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .database.session_manager import get_async_session
from .redis_utils import get_redis_client

log = logging.getLogger(__name__)


def inject_redis[
    RT, **P
](func: Callable[..., Awaitable[RT]],) -> Callable[..., Awaitable[RT]]:
    if not inspect.iscoroutinefunction(func):
        raise TypeError("function must be a coroutine")

    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        if "redis" not in kwargs.keys():
            _redis_client = get_redis_client()
            kwargs["redis"] = _redis_client
        return await func(*args, **kwargs)

    return _wrapper


def inject_asyncpg_session[
    RT, **P
](func: Callable[..., Awaitable[RT]],) -> Callable[..., Awaitable[RT]]:
    """injects asyncpg session into the function as keyword argument.

    Raises:
        TypeError: Generates an error if the function is not a coroutine.
        TypeError: Generates an error if the session is not an AsyncSession.
        e: Raise the exception and rollback the session when there is sqlalchemy error.

    Returns:
        _type_: Returns the function with the session as a keyword argument.
    """

    if not inspect.iscoroutinefunction(func):
        raise TypeError("function must be a coroutine")

    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        if "session" not in kwargs or not isinstance(
            kwargs.get("session", object()), AsyncSession
        ):
            raise TypeError("session must be an AsyncSession")
        async with await anext(get_async_session()) as session:
            kwargs["session"] = session
            try:
                return await func(*args, **kwargs)
            except SQLAlchemyError as e:
                log.error(e)
                await session.rollback()
                raise e
            finally:
                await session.close()

    return cast(Callable[..., Awaitable[RT]], _wrapper)
