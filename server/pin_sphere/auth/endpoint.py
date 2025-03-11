from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from core.database.session_manager import get_async_session

from . import schemas, service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        403: {"description": "Forbidden"},
    },
    default_response_class=ORJSONResponse,
)


@router.post("/login")
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    return await service.login_user(form_data, response, session)


@router.post("/refresh")
async def refresh_access_token(
    token: str | None = Cookie(None, alias="refresh_token"),
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return await service.refresh_access_token(token, db)


@router.post("/signup", status_code=204)
async def signup(
    credentials: schemas.SignupUser = Body(),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Signup with pin_sphere
    - **body**: credentials to log in with pin_sphere.
    """
    return await service.signup_user(credentials, session)


@router.post("/google")
async def google_auth(
    postBody: schemas.GoogleOauthPostBody,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Exchange Google auth code for tokens, verify user, and return JWT
    """
    return await service.exchange_google_auth(postBody.code, session)
