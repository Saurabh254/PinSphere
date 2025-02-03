from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

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
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    return await service.login_user(form_data, session)


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
