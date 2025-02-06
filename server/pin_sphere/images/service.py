from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from core import storage
from core.models import Images, User
from core.models.images import ImageProcessingStatus
from core.types import FileContentType
from pin_sphere.base_exception import ServerError
from pin_sphere.images.exceptions import (
    ImageAlreadyExistsError,
    ImageNotFoundError,
)
from pin_sphere.images.utils import get_image_key


async def get_image(
    image_id: UUID, session: AsyncSession, user: User | None = None
) -> Images | None:
    """
    Retrieve an image from the database by its ID.

    Args:
        image_id (UUID): The unique identifier of the image to retrieve.
        session (AsyncSession): The SQLAlchemy asynchronous session to use for the query.
        user (User | None): The user performing the query.

    Returns:
        Images: The image object if found, otherwise None.
    """
    stmt = select(Images).filter_by(id=image_id)
    if user:
        stmt = stmt.filter_by(username=user.username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_image(user: User, image_id: UUID, session: AsyncSession) -> None:
    """
    Delete an image from the database by its ID.

    Args:
        user (User): The user performing the deletion.
        image_id (UUID): The unique identifier of the image to delete.
        session (AsyncSession): The SQLAlchemy asynchronous session to use for the query.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    image = await get_image(image_id, session)
    if not image:
        raise ImageNotFoundError
    image.deleted = True
    await session.commit()


async def save_image(
    user: User, image_key: str, session: AsyncSession, description: str | None = None
) -> Images:
    """
    Save an image to the database.

    Args:
        user (User): The user uploading the image.
        image_key (str): The key of the image to save.
        description(str): this is the description of the image.
        session (AsyncSession): The SQLAlchemy asynchronous session to use for the query.

    Returns:
        None
    """
    stmt = select(Images).filter_by(image_key=image_key)
    existing_image = await session.execute(stmt)
    if existing_image.scalar_one_or_none():
        raise ImageAlreadyExistsError
    image = Images(
        username=user.username,
        image_key=image_key,
        status=ImageProcessingStatus.PROCESSING,
        description=description,
    )
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image


def get_image_pre_signed_url(user: User, ext: FileContentType) -> dict[str, str]:
    image_key = get_image_key(user.username, ext)

    res = storage.create_presigned_post(image_key, ext)
    if not res:
        raise ServerError(status_code=500, message="Failed to create presigned URL")
    return res


async def get_images(user: User, session: AsyncSession):
    stmt = (
        select(Images)
        .filter_by(username=user.username)
        .order_by(Images.created_at.desc())
    )
    return await paginate(session, stmt)
