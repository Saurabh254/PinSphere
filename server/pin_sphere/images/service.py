from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


def get_image(user: User, image_id: str , session: AsyncSession):
    return None


def delete_image(user: User, image_id: str, session: AsyncSession):
    return None


def save_image(current_user, file, username: str, session: AsyncSession):
    return None
