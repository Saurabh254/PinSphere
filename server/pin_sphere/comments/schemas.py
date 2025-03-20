from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    content_id: UUID


class SlimCommentResponse(CommentBase):
    id: UUID
    user_id: UUID
    content_id: UUID
    parent_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


class CommentResponse(SlimCommentResponse):
    replies: List["SlimCommentResponse"] = []

    class Config:
        orm_mode = True
