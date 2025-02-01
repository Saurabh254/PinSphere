# type: ignore

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from core.database.session_manager import get_async_session
from core.models import User
from . import service, schemas
from core.authflow import auth


router = APIRouter(prefix="/images", tags=["images"])


@router.post("/", response_model=schemas.ImageResponse)
async def upload_image(
    username: str,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Upload a new image for a user
    """
    try:
        # Pass current_user to the service function as the first argument
        image = await service.save_image(current_user, file.file, username, session)  # type: ignore
        return image
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{image_id}", response_model=schemas.ImageResponse)
async def get_image_by_id(
    image_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Get image details by ID
    """
    image = await service.get_image(current_user, image_id, session)  # type: ignore
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
