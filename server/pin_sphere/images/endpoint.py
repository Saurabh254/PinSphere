# type: ignore

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from starlette import status

from core.database.session_manager import get_async_session
from core.models import User
from core.types import FileContentType
from . import service, schemas
from core.authflow import auth
from fastapi_pagination import Page

router = APIRouter(prefix="/images", tags=["images"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=schemas.ImageResponse
)
async def upload_image(
    image_key: str,
    description: str | None = None,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Upload a new image for a user
    """
    return await service.save_image(current_user, image_key, description, session)  # type: ignore


@router.get("", response_model=Page[schemas.ImageResponse])
async def get_images(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Get all images for a user
    """
    return await service.get_images(current_user, session)


@router.get("/upload_url")
def get_pre_signed_url(
    ext: FileContentType,
    user: User = Depends(auth.get_current_user),
):
    """
    Get pre-signed URL for image upload
    """

    return service.get_image_pre_signed_url(user, ext)


@router.get("/{image_id}", response_model=schemas.ImageResponse)
async def get_image_by_id(
    image_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Get image details by ID
    """
    image = await service.get_image(image_id, session, current_user)  # type: ignore
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image  # type: ignore


@router.delete("/{image_id}", status_code=204)
async def delete_image(
    image_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(
        auth.get_current_user
    ),  # Add the current_user dependency
):
    """
    Delete an image by ID
    """
    success = await service.delete_image(current_user, image_id, session)  # type: ignore
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"status": "success"}
