import time
import uuid

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from core.authflow.auth import (
    create_access_token,
    create_refresh_token,
    verify_and_return_refresh_token_payload,
)
from core.authflow.service import verify_password
from core.models import User
from logging_conf import log
from pin_sphere.users import service as user_service

from . import exceptions, schemas


async def login_user(
    credentials: OAuth2PasswordRequestForm, response: Response, session: AsyncSession
):
    user: User = await user_service.get_user(session, credentials.username)
    if not user:
        raise exceptions.UserNotFound(message="User not found with given credentials")
    is_valid_password = verify_password(
        user.password, user.password_salt, credentials.password
    )
    if not is_valid_password:
        raise exceptions.InvalidUsernameOrPassword()
    jti = uuid.uuid4()
    access_token_data = {
        "sub": credentials.username,
        "jti": str(jti),
        "role": ["user"],
    }
    refresh_token_data = {
        "sub": credentials.username,
        "jti": str(jti),
        "iat": int(time.time()),
        "scope": ["user"],
    }

    refresh_token = await create_refresh_token(refresh_token_data)

    response.set_cookie("refresh_token", refresh_token)
    access_token = await create_access_token(access_token_data)

    return {"access_token": access_token, "token_type": "bearer"}


async def refresh_access_token(token: str, session: AsyncSession):
    validation_result = await verify_and_return_refresh_token_payload(token)
    if not validation_result:
        raise exceptions.InvalidRefreshToken()
    data = {
        "sub": validation_result.get("sub"),
        "role": ["user"],
        "jti": str(validation_result.get("jti")),
    }
    access_token = await create_access_token(data)
    log.debug(
        f"Refresh access token for the user [{validation_result.get('sub')}]",
        extra={
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": token,
        },
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def signup_user(credentials: schemas.SignupUser, session: AsyncSession) -> None:
    user = await user_service.get_user(session, credentials.username)
    if user:
        raise exceptions.UserAlreadyExists()

    await user_service.create_user(session, credentials)
