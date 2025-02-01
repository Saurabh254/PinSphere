from typing import BinaryIO
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


def get_image(user: User, image_id: str, session: AsyncSession):
    return None


def delete_image(user: User, image_id: UUID, session: AsyncSession):
    return None


def save_image(
    current_user: User, file: BinaryIO, username: str, session: AsyncSession
):
    return None
