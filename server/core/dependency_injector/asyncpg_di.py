import functools
import inspect
import logging

from typing import Awaitable, Callable, cast

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.session_manager import async_session
from .errors import InjectError

log = logging.getLogger("pin_sphere")


def inject_asyncpg_session[RT, **P](
    func: Callable[P, Awaitable[RT]],
) -> Callable[P, Awaitable[RT]]:
    """
    Decorator to inject an AsyncSession into the decorated coroutine function.

    Returns:
        Callable: A decorator that injects an AsyncSession into the decorated coroutine function.

    Example:
        basic usage:

        >>> @inject_asyncpg_session
        >>> async def my_function(session: AsyncSession = Inject()):
        >>>    # Use the session here
        >>>    ...

    """
    if not inspect.iscoroutinefunction(func):
        raise TypeError("function must be a coroutine")
        # Get the function's signature
    sig = inspect.signature(func)

    # Check if the parameter has Injected as its default value
    db_param = next(
        (
            name
            for name, param in sig.parameters.items()
            if param.annotation == AsyncSession and param.default != param.empty
        ),
        None,
    )

    if not db_param:
        raise InjectError(
            f"Function {func.__name__} must have a AsyncSession parameter "
            "with default value of Inject()"
        )

    @functools.wraps(func)
    async def _wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        # Create a new signature to modify parameters
        bound_arguments = sig.bind(*args, **kwargs)
        bound_arguments.apply_defaults()
        # # Check if db is already provided
        if (
            db_param in bound_arguments.arguments
            and bound_arguments.arguments[db_param]
            and isinstance(bound_arguments.arguments[db_param], AsyncSession)
        ):
            return await func(*args, **kwargs)

        # Create a new session and inject it if the provided session is of type Inject
        session = async_session()
        bound_arguments.arguments[db_param] = session
        try:
            result = await func(*bound_arguments.args, **bound_arguments.kwargs)
            return result
        except SQLAlchemyError as e:
            # Log the error and rollback the session in case of an exception
            log.error(e)
            await session.rollback()
            raise e
        finally:
            await session.close()

    return cast(Callable[..., Awaitable[RT]], _wrapper)
