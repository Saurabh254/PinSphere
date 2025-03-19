from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import defer, joinedload, selectinload

from core.models import User
from core.models.content import Comment, CommentLike
from .errors import CommentNotFoundError



async def create_comment(user, content_id: UUID, text: str, session: AsyncSession):
    comment = Comment(content_id=content_id, user_id=user.id, text=text)
    session.add(comment)
    await session.commit()



async def get_comments(content_id: UUID, session: AsyncSession):
    stmt = select(Comment).where(Comment.content_id == content_id)
    return await paginate(session, stmt)


async def create_reply(user, comment_id: UUID, text: str, session: AsyncSession):
    result = await session.execute(select(Comment).where(Comment.id == comment_id))
    parent_comment = result.scalar_one_or_none()
    if not parent_comment:
        raise CommentNotFoundError()

    reply = Comment( content_id=parent_comment.content_id, user_id=user.id, text=text, parent_id=comment_id)
    session.add(reply)
    await session.commit()



async def get_comment(comment_id: UUID, session: AsyncSession, user: User):
    query = (
        select(Comment)
        .options(
            joinedload(Comment.replies),
            joinedload(Comment.user))

        .where(Comment.id == comment_id)
    )

    result = await session.execute(query)
    comment =  result.unique().scalar_one_or_none()
    if not comment:
        raise CommentNotFoundError()
    return comment


async def delete_comment(user, comment_id: UUID, session: AsyncSession):
    result = await session.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise CommentNotFoundError()
    await session.delete(comment)
    await session.commit()



async def toggle_like_comment(user, comment_id: UUID, like: bool, session: AsyncSession):
    """
    Like or unlike a comment
    """
    result = await session.execute(
        select(CommentLike).where(CommentLike.comment_id == comment_id, CommentLike.user_id == user.id)
    )
    existing_like = result.scalar_one_or_none()

    if like:
        if not existing_like:
            new_like = CommentLike(user_id=user.id, comment_id=comment_id)
            session.add(new_like)
    else:
        if existing_like:
            await session.delete(existing_like)

    await session.commit()
