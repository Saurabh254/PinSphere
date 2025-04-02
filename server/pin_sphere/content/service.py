# type: ignore
from typing import Any

import numpy
import torch
from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sentence_transformers import util
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from core import storage
from core.embedding_generation import generate_embeddings
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


async def search_content_by_context(
    text: str,
    session: AsyncSession,
    page_size: int = 10,
    page: int = 1,
) -> Page[Content]:
    """
    Search for similar documents based on embedding similarity and return paginated results.
    Uses sentence-BERT to filter out non-relevant content based on a similarity threshold.
    Also filters out items that have a similarity score above max_similarity_threshold.

    Args:
        text: The search text to find similar content
        session: Database session
        page_size: Number of items per page
        page: Current page number
        similarity_threshold: Minimum similarity score for content to be included
        max_similarity_threshold: Maximum similarity score for content to be included

    Returns:
        Paginated Content objects filtered by embedding similarity
    """
    # Generate embedding for query
    query_embedding = generate_embeddings(text)

    # First, fetch more results than needed to allow for filtering
    # Using a buffer multiplier to ensure we have enough data to filter
    buffer_multiplier = 3
    fetch_size = page_size * buffer_multiplier

    # Perform vector similarity search with a larger result set
    query = (
        select(Content)
        .filter(Content.deleted.is_(False), Content.embedding.is_not(None))
        .options(joinedload(Content.user))
        .order_by(Content.embedding.cosine_distance(query_embedding))
        .limit(fetch_size)
    )

    # Execute initial query
    result = await session.execute(query)
    candidate_docs = result.scalars().all()

    # Convert query embedding to tensor
    query_tensor = torch.tensor([query_embedding], dtype=torch.float)

    # Filter candidates using sentence-BERT similarity scores
    filtered_docs = []
    prev = -1
    for doc in candidate_docs:
        doc_tensor = torch.tensor(numpy.array(doc.embedding), dtype=torch.float)
        similarity = util.pytorch_cos_sim(query_tensor, doc_tensor).item()

        # Only include documents with similarity between thresholds
        if prev == -1 or prev - similarity < 0.1:
            filtered_docs.append(doc)
            prev = similarity

    # Calculate total filtered count for pagination
    total_count = len(filtered_docs)

    # Manual pagination on filtered results
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_count)
    paginated_docs = filtered_docs[start_idx:end_idx] if start_idx < total_count else []  # type: ignore

    # Create custom Page object
    return Page[Content](
        items=paginated_docs, total=total_count, page=page, size=page_size
    )
