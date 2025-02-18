# type: ignore

from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.authflow import auth
from core.database.session_manager import get_async_session
from core.models import User
from core.types import FileContentType
from pin_sphere.content.exceptions import ContentNotFoundError

from . import schemas, service

router = APIRouter(prefix="/content", tags=["content"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.ContentResponse
)
async def upload_content(
    content_key: str = Body(),
    description: str | None = Body(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Upload a new image for a user
    """
    return await service.save_content(
        current_user, content_key, description=description, session=session
    )  # type: ignore


@router.get("", response_model=Page[schemas.ContentResponse])
async def get_contents(
    session: AsyncSession = Depends(get_async_session),
    username: str | None = Query(None, description="Username or None"),
):
    """
    Get all images for a user
    """
    return await service.get_contents(username, session)


@router.get("/upload_url")
def get_pre_signed_url(
    ext: FileContentType,
    user: User = Depends(auth.get_current_user),
):
    """
    Get pre-signed URL for image upload
    """
    return service.get_content_pre_signed_url(user, ext)


@router.get("/{content_key}", response_model=schemas.ContentResponse)
async def get_image_by_id(
    content_key: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Get image details by ID
    """
    image = await service.get_content(content_key, session, current_user)  # type: ignore
    if not image:
        raise ContentNotFoundError()
    return image  # type: ignore


@router.delete("/{content_key}", status_code=204)
async def delete_image(
    content_key: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Delete an image by ID
    """
    await service.delete_image(current_user, content_key, session)  # type: ignore
    return {"status": "success"}
