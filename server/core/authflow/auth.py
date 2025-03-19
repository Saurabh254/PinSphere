from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Annotated, Any

import jwt
from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from core.database.session_manager import get_async_session
from core.models import User
from logging_conf import log


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


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


def create_refresh_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRATION_SECONDS
        )
    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt: str = jwt.encode(  # type: ignore
        to_encode, settings.AUTH_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(  # type: ignore
            token,
            settings.AUTH_SECRET,
            algorithms=settings.ALGORITHM,
            options={"verify_exp": False},
        )
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


def get_refresh_token_key(x: str):
    return f"refresh_tokens:{x}"


async def verify_and_return_refresh_token_payload(token: str) -> dict[str, str] | None:
    try:
        return decode_access_token(token)

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    # TODO: Store and check revoked tokens from redis

    # jti = decoded.get("jti")
    # user_id: str = decoded.get("sub")
    # redis_client = await anext(get_redis_client())
    # spacename = get_refresh_token_key(user_id)
    # key = await redis_client.hget(spacename, jti)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login", description="Get token from the login endpoint"
)


GOOGLE_CLIENT_ID = "your-google-client-id.apps.googleusercontent.com"


async def get_optional_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> User | None:
    """
    Get current user from JWT (issued by your system).
    """
    decoded = decode_access_token(token)
    if decoded:
        stmt = select(User).filter(User.id == decoded.get("sub"))
        result = await session.execute(stmt)
        return result.scalars().first()

    raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    user: User | None = Depends(get_optional_current_user),
) -> User:
    """
    Get current user from token
    """
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_auth_token(authorization: Annotated[str, Header(alias="Authorization")]) -> str:
    scheme, token = authorization.split(" ", 1)
    if scheme != "Bearer":
        return token
    raise HTTPException(status_code=401, detail="Unauthorized")




if __name__ == "__main__":
    print(create_access_token({"user_id": "test"}))
