from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.authflow import auth
from core.database.session_manager import get_async_session
from core.models import User

from . import schemas, service

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def add_comment(
    content_id: UUID = Body(),
    text: str = Body(),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Add a comment to a content item
    """
    await service.create_comment(current_user, content_id, text, session)  # type: ignore


@router.get("", response_model=Page[schemas.CommentResponse])
async def get_comments(
    content_id: UUID = Query(..., description="ID of the content"),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Get all comments for a content item
    """
    return await service.get_comments(content_id, session)


@router.post("/{comment_id}/reply", status_code=status.HTTP_204_NO_CONTENT)
async def reply_to_comment(
    comment_id: UUID = Path(description="ID of the comment"),
    text: str = Body(),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Reply to a comment
    """
    await service.create_reply(current_user, comment_id, text, session)  # type: ignore


@router.get("/{comment_id}", response_model=schemas.CommentResponse)
async def get_comment_by_id(
    comment_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Get comment details by ID
    """
    return await service.get_comment(comment_id, session, current_user)  # type: ignore


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Delete a comment by ID
    """
    await service.delete_comment(current_user, comment_id, session)  # type: ignore
    return {"status": "success"}


@router.post("/{comment_id}/like", status_code=status.HTTP_201_CREATED)
async def toggle_like_comment(
    current_user: User = Depends(auth.get_current_user),
    comment_id: UUID = Path(description="ID of the comment"),
    like: bool = Query(True),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Like or dislike a comment
    """
    await service.toggle_like_comment(current_user, comment_id, like, session)
