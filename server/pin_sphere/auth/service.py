from sqlalchemy.ext.asyncio import AsyncSession

from core.authflow.auth import create_access_token
from core.authflow.service import verify_password
from core.models import User
from pin_sphere.users import service as user_service
from . import schemas, exceptions


async def login_user(
    credentials: schemas.LoginUser, session: AsyncSession
) -> dict[str, str]:
    user: User = await user_service.get_user(session, credentials.username)
    if not user:
        raise exceptions.UserNotFound(message="User not found with given credentials")
    is_valid_password = verify_password(
        user.password, user.password_salt, credentials.password.get_secret_value()
    )
    if not is_valid_password:
        raise exceptions.InvalidUsernameOrPassword()
    data = {
        "username": credentials.username,
        "role": ["user"],
    }
    access_token = create_access_token(data)
    return {"access_token": access_token, "token_type": "bearer"}


async def signup_user(credentials: schemas.SignupUser, session: AsyncSession) -> None:
    user = await user_service.get_user(session, credentials.username)
    if user:
        raise exceptions.UserAlreadyExists()

    await user_service.create_user(session, credentials)
