import logging
from typing import Any
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core import storage
from core.models import Content, User
from core.models.content import ContentProcessingStatus
from core.types import FileContentType
from pin_sphere.base_exception import ServerError
from pin_sphere.content.exceptions import (
    ContentAlreadyExistsError,
    ContentNotFoundError,
)
from pin_sphere.content.utils import get_content_key

from . import tasks

log = logging.getLogger(__name__)


async def get_content(
    content_id: UUID, session: AsyncSession, user: User | None = None
) -> Content | None:
    stmt = select(Content).filter_by(id=content_id, deleted=False)
    if user:
        stmt = stmt.filter_by(username=user.username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_content(user: User, content_id: UUID, session: AsyncSession) -> None:
    content = await get_content(content_id, session, user)
    if not content or content.username != user.username:
        raise ContentNotFoundError
    content.deleted = True
    await session.commit()


async def save_content(
    user: User, content_key: str, session: AsyncSession, description: str | None = None
) -> Content:
    stmt = select(Content).filter_by(content_key=content_key)
    existing_content = await session.execute(stmt)
    if existing_content.scalar_one_or_none():
        raise ContentAlreadyExistsError

    content = Content(
        username=user.username,
        content_key=content_key,
        status=ContentProcessingStatus.PROCESSING,
        description=description,
    )
    session.add(content)
    await session.commit()
    await session.refresh(content)

    tasks.generate_blurhash.delay(content.id, content.content_key)  # type: ignore
    return content


def get_content_pre_signed_url(user: User, ext: FileContentType) -> dict[str, str]:
    content_key = get_content_key(user.username, ext)
    res = storage.create_presigned_post(content_key, ext)
    if not res:
        raise ServerError(status_code=500, message="Failed to create presigned URL")
    return res


async def get_contents(username: str | None, session: AsyncSession):
    stmt = (
        select(Content)
        .filter_by(deleted=False)
        .filter_by(status=ContentProcessingStatus.PROCESSED)
        .order_by(Content.created_at.desc())
    )
    if username:
        stmt = stmt.filter_by(username=username)
    return await paginate(session, stmt)


def update_content(
    content_id: str, session: Session, /, **kwargs: dict[str, Any]
) -> None:
    content: Content | None = session.query(Content).get(content_id)
    if not content:
        raise ContentNotFoundError
    for key, value in kwargs.items():
        setattr(content, key, value)

    session.commit()
