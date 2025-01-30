from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.datastructures import FormData

from core.authflow.auth import create_access_token
from core.authflow.service import verify_password
from core.models import User
from pin_sphere.users import service as user_service
from . import schemas, exceptions


async def login_user(
    credentials: OAuth2PasswordRequestForm, session: AsyncSession
) -> dict[str, str]:
    user: User = await user_service.get_user(session, credentials.username)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not user:
        raise credentials_exception
    is_valid_password = verify_password(
        user.password, user.password_salt, credentials.password
    )
    if not is_valid_password:
        raise exceptions.InvalidUsernameOrPassword()
    data = {
        "sub": credentials.username,
        "role": ["user:read", "user:write"],
    }
    access_token = create_access_token(data)
    return {"access_token": access_token, "token_type": "bearer"}


async def signup_user(credentials: schemas.SignupUser, session: AsyncSession) -> None:
    user = await user_service.get_user(session, credentials.username)
    if user:
        raise exceptions.UserAlreadyExists()

    await user_service.create_user(session, credentials)
