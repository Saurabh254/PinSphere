from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, computed_field

from config import settings


class ContentStatus(str, Enum):
    PROCESSED = "PROCESSED"
    PROCESSING = "PROCESSING"


class ContentCreate(BaseModel):
    username: str
    content_uuid: UUID
    description: Optional[str] = Field(
        "No description provided", description="Description of the content"
    )


class ContentMeta(BaseModel):
    height: int
    width: int


class ContentResponse(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the content")
    username: str = Field(..., description="Username of the content owner")
    content_key: str = Field(
        ..., description="Key of the content in storage", exclude=True
    )
    status: ContentStatus = Field(..., description="Processing status of the content")
    blurhash: Optional[str] = Field(
        None, description="Blurhash for fast loading previews"
    )
    description: Optional[str] = Field(
        "No description provided", description="Content description"
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the content was created"
    )
    raw_metadata: Optional[dict[str, Any]] = Field(
        None, exclude=True, alias="_metadata"
    )

    @computed_field
    def url(self) -> HttpUrl:
        return HttpUrl(
            f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.content_key}"
        )

    @computed_field
    def metadata(self) -> Optional[ContentMeta]:
        return ContentMeta(**self.raw_metadata) if self.raw_metadata else None
