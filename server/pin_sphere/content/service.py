from typing import Any

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from core import storage
from core.models import Content, User
from core.models.content import ContentLikes, ContentProcessingStatus
from core.types import FileContentType
from pin_sphere.base_exception import ServerError
from pin_sphere.content.exceptions import (
    ContentAlreadyExistsError,
    ContentNotFoundError,
)
from pin_sphere.content.utils import get_content_key

from . import tasks


async def get_content(
    content_id: str, session: AsyncSession, user: User | None = None
) -> Content | None:
    stmt = (
        select(Content)
        .options(joinedload(Content.user))
        .filter_by(id=content_id, deleted=False)
    )
    if user:
        stmt = stmt.filter_by(user_id=user.id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def delete_content(user: User, content_id: str, session: AsyncSession) -> None:
    content = await get_content(content_id, session, user)
    if not content or content.user_id != user.id:
        raise ContentNotFoundError
    content.deleted = True
    await session.commit()


async def save_content(
    user: User,
    content_key: str,
    session: AsyncSession,
    ext: FileContentType,
    description: str | None = None,
) -> Content:
    stmt = select(Content).filter_by(content_key=content_key)
    existing_content = await session.execute(stmt)
    if existing_content.scalar_one_or_none():
        raise ContentAlreadyExistsError
    content = Content(
        user_id=user.id,
        content_key=content_key,
        status=ContentProcessingStatus.PROCESSED,
        description=description,
    )
    if ext in [ext.PNG, ext.JPEG, ext.GIF]:
        content.status = ContentProcessingStatus.PROCESSING
    else:
        content._metadata = {"width": 400, "height": 200, "content_type": ext.value}  # type: ignore
    session.add(content)
    await session.commit()
    await session.refresh(content)

    if ext.PNG or ext.JPEG or ext.GIF:
        tasks.generate_blurhash.delay(content.id, content.content_key)  # type: ignore
        tasks.generate_content_embedding_and_save.delay(content.content_key)
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
        .options(
            joinedload(Content.user)  # Corrected
        )
        .filter_by(status=ContentProcessingStatus.PROCESSED)
        .order_by(Content.created_at.desc())
    )

    if username:
        stmt = stmt.filter(Content.user.has(username=username))
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


async def toggle_like(
    user: User, content_id: str, like: bool, session: AsyncSession, /
) -> None:
    content = await get_content(content_id, session, None)

    if not content:
        raise ContentNotFoundError
    content.likes += 1
    stmt = select(ContentLikes).filter(
        ContentLikes.content_id == content_id,
        ContentLikes.user_id == user.id,
    )
    result = await session.execute(stmt)
    content_like_model: ContentLikes = result.scalar_one_or_none()
    if content_like_model:
        content_like_model.toggle_likes()
    else:
        content_like_model = ContentLikes(content_id=content_id, user_id=user.id)
        session.add(content_like_model)

    await session.commit()


def get_user_contents(user: User, session: AsyncSession):
    stmt = select(Content).filter_by(user_id=user.id)
    return paginate(session, stmt)
