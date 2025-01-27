from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from core.database.session_manager import get_async_session
from core.models import User
import logging


log = logging.getLogger(__name__)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    """Create JWT access token
    :param data: data
    :param expires_delta: expires delta
    :return: JWT access token
    """
    data.update({"exp": str(datetime.now() + expires_delta)})
    encode = jwt.encode(data, settings.AUTH_SECRET, algorithm=settings.ALGORITHM) #type: ignore
    return encode


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.AUTH_SECRET, algorithm=settings.ALGORITHM) #type: ignore
    except jwt.DecodeError:
        return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        log.error(e)
        raise e


async def get_current_user(
    token: str = Depends(HTTPBearer(description="this is description")),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    decoded: dict[str, Any]|None = decode_access_token(token)
    if decoded is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    stmt = select(User).filter(User.username == decoded.get("sub"))
    result = await session.execute(stmt)
    return result.scalars().first()


if __name__ == "__main__":
    print(create_access_token({"username": "test", "password": "<PASSWORD>"}))
