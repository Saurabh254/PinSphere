import time
import uuid

import faker
import httpx
import requests
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from google.oauth2 import id_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from config import settings
from core.authflow.auth import (
    create_access_token,
    create_refresh_token,
    verify_and_return_refresh_token_payload,
)
from core.authflow.service import verify_password
from core.models import User
from core.models.user import AuthType
from logging_conf import log
from pin_sphere.users import service as user_service

from . import exceptions, schemas

fake = faker.Faker()

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
        "sub": str(user.id),
        "jti": str(jti),
        "role": ["user"],
    }
    refresh_token_data = {
        "sub": str(user.id),
        "jti": str(jti),
        "iat": int(time.time()),
        "scope": ["user"],
    }

    refresh_token = create_refresh_token(refresh_token_data)

    response.set_cookie("refresh_token", refresh_token)
    access_token = create_access_token(access_token_data)

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
    access_token = create_access_token(data)
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
from google.auth.transport import requests as google_requests

async def verify_google_token(token: str) -> dict | None:
    """
    Verify Google ID Token and return user data
    """
    try:
        return id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID)
    except ValueError:
        return None

async def exchange_google_auth(code, session):

        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH2_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            token_data = response.json()

        if "id_token" not in token_data:
            raise HTTPException(status_code=400, detail="Invalid Google token")

        # Verify ID Token and extract user info
        id_token_info = await verify_google_token(token_data["id_token"])
        if not id_token_info:
            raise HTTPException(status_code=401, detail="Invalid Google token")

        email = id_token_info.get("email")
        full_name = id_token_info.get("name")

        # Check if user exists, if not create
        stmt = select(User).filter(User.email == email)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            user = User(email=email, username=fake.user_name(),name=full_name, auth_type=AuthType.google)
            session.add(user)
            await session.commit()

        # Generate JWT token for authentication

        jwt_token = create_access_token({"sub": str(user.id), "jti": str(uuid.uuid4()),
        "iat": int(time.time()),
        "scope": ["user"],})

        return {"access_token": jwt_token}
