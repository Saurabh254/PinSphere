from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


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
    replies: List["SlimCommentResponse"]  = []

    class Config:
        orm_mode = True
