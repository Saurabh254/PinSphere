from logging_conf import log
from datetime import datetime, timedelta
from typing import Annotated, Any
from datetime import UTC
import jwt
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from core.database.session_manager import get_async_session
from core.models import User
from enum import Enum

from core.redis_utils import get_redis_client



class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


async def create_access_token(
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

async def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_SECONDS)
    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt: str = jwt.encode(to_encode, settings.AUTH_SECRET, algorithm=settings.ALGORITHM)
    return encoded_jwt



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

get_refresh_token_key = lambda x: f"refresh_tokens:{x}"

async def is_valid_refresh_token(token: str) -> dict[str, str]:
    try:
        decoded = decode_access_token(token)
        if decoded is None:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    jti = decoded.get('jti' )
    user_id: str = decoded.get('sub')

    redis_client = await anext(get_redis_client())
    spacename = get_refresh_token_key(user_id)
    key = await redis_client.hget(spacename, jti)
    return decoded



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login", description="Get token from the login endpoint"
)


async def get_optional_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User | None:
    """
    Get current user from token
    :param token: token
    :param session: session

    """
    decoded: dict[str, Any] | None = decode_access_token(token)
    if decoded is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    stmt = select(User).filter(User.username == decoded.get("sub"))
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_current_user(
    user: User | None = Depends(get_optional_current_user),
) -> User:
    """
    Get current user from token
    """
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_auth_token(authorization: Annotated[str, Header(alias='Authorization')]) -> str:
    scheme, token = authorization.split(" ", 1)
    if scheme != "Bearer":
        return token
    raise HTTPException(status_code=401, detail="Unauthorized")

    ...
if __name__ == "__main__":
    print(create_access_token({"username": "test", "password": "<PASSWORD>"}))
