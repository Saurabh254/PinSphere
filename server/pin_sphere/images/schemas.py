from datetime import datetime
from typing import ClassVar, Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl, computed_field
from enum import Enum

from config import settings


class ImageStatus(str, Enum):
    PROCESSED = "PROCESSED"
    PROCESSING = "PROCESSING"


class ImageCreate(BaseModel):
    username: str
    image_uuid: UUID
    description: str|None = Field(default="No description provided", description="Description of the image")


class ImageResponse(BaseModel):
    id: UUID = Field(..., description="The unique identifier of the image")
    username: str = Field(..., description="The username of the image owner")
    image_key: str = Field(..., description="The key of the image in storage", exclude=True)  # not included in the schemas
    status: ImageStatus = Field(..., description="The processing status of the image")
    blurhash: Optional[str] = Field(None, description="The blurhash of the image for fast loading previews")
    description: str|None = Field(default="No description provided", description="Description of the image")
    created_at: datetime = Field(..., description="The timestamp when the image was created")
    
    @computed_field
    def url(self) -> HttpUrl:
        return HttpUrl(
            f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.image_key}"
        )
