from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query
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
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.SlimContentResponse
)
async def upload_content(
    content_key: str = Body(),
    description: str | None = Body(None),
    ext: FileContentType = Body(),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Upload a new image for a user
    """
    return await service.save_content(
        current_user, content_key, description=description, session=session, ext=ext
    )  # type: ignore


@router.get("", response_model=Page[schemas.ContentResponse])
async def get_contents(
    session: AsyncSession = Depends(get_async_session),
    username: Optional[str] = Query(None, description="Username or None"),
):
    """
    Get all images for a user
    """
    return await service.get_contents(username, session)


@router.get("/me", response_model=Page[schemas.SlimContentResponse])
async def get_user_contents(
    current_user: User = Depends(auth.get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get all contents of a user
    """
    return await service.get_user_contents(current_user, session)


@router.get("/upload_url")
def get_pre_signed_url(
    ext: FileContentType,
    user: User = Depends(auth.get_current_user),
):
    """
    Get pre-signed URL for image upload
    """
    return service.get_content_pre_signed_url(user, ext)


@router.get("/{content_id}", response_model=schemas.ContentResponse)
async def get_image_by_id(
    content_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Get image details by ID
    """
    image = await service.get_content(content_id, session, current_user)  # type: ignore
    if not image:
        raise ContentNotFoundError()
    return image  # type: ignore


@router.delete("/{content_id}", status_code=204)
async def delete_image(
    content_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Delete an image by ID
    """
    await service.delete_image(current_user, content_id, session)  # type: ignore
    return {"status": "success"}


@router.post("/{content_id}/like", status_code=status.HTTP_201_CREATED)
async def toggle_like_content(
    current_user: User = Depends(auth.get_current_user),
    content_id: str = Path(description="id of the content "),
    like: bool = Query(True),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Like or dislike an image

    """
    await service.toggle_like(current_user, content_id, like, session)
