import logging
from datetime import datetime, timedelta
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from core.database.session_manager import get_async_session
from core.models import User

log = logging.getLogger("main")


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    """Create JWT access token
    :param data: data
    :param expires_delta: expires delta
    :return: JWT access token
    """
    data.update({"exp": datetime.now() + expires_delta})
    encode = jwt.encode(data, settings.AUTH_SECRET, algorithm=settings.ALGORITHM)  # type: ignore
    return encode


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.AUTH_SECRET, algorithms=settings.ALGORITHM)  # type: ignore
    except jwt.DecodeError as e:
        log.debug("Error decoding access token: %s", e)
        return None
    except jwt.ExpiredSignatureError:
        log.debug("Error expired access token")
        return None
    except jwt.InvalidTokenError:
        log.debug("Error invalid access token")
        return None
    except Exception as e:
        log.error(e)
        raise e


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login", description="Get token from the login endpoint"
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Get current user from token
    :param token: token
    :param session: session

    """
    decoded: dict[str, Any] | None = decode_access_token(token)
    if decoded is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    stmt = select(User).filter(User.username == decoded.get("username"))
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


if __name__ == "__main__":
    print(create_access_token({"username": "test", "password": "<PASSWORD>"}))
