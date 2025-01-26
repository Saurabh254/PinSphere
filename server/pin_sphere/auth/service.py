from sqlalchemy.ext.asyncio import AsyncSession

from core.authflow.auth import create_access_token
from core.authflow.service import verify_password
from pin_sphere.users import service as user_service
from pin_sphere.users import schemas as user_schemas
from . import schemas, exceptions



async def login_user(credentials:schemas.LoginUser, session: AsyncSession)-> dict[str, str]:
    user = await user_service.get_user(session, credentials.username)
    if not user:
        raise exceptions.UserNotFound(message="User not found with given credentials")
    is_valid_password = verify_password(user.hashed_password, user.password_salt, credentials.hashed_password)
    if not is_valid_password:
        raise exceptions.InvalidUsernameOrPassword()
    data = {
        "username": credentials.username,
        "role": ["user"],
    }
    access_token = create_access_token(data)
    return {"access_token": access_token, "token_type": "bearer"}


async def signup_user(credentials: schemas.SignupUser, session: AsyncSession)-> dict:
    user = await user_service.get_user(session, credentials.username)
    if not user:
        raise exceptions.UserNotFound(message="User not found with given credentials")

    await user_service.create_user(session, user)
