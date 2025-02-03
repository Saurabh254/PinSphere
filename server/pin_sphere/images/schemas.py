from typing import Optional
from uuid import UUID
from pydantic import BaseModel, HttpUrl, computed_field
from enum import Enum

from config import settings


class ImageStatus(str, Enum):
    PROCESSED = "PROCESSED"
    PROCESSING = "PROCESSING"


class ImageCreate(BaseModel):
    username: str
    image_uuid: UUID


class ImageResponse(BaseModel):
    id: UUID
    username: str
    image_key: str
    status: ImageStatus
    blurhash: Optional[str]

    @computed_field
    def url(self) -> HttpUrl:
        return HttpUrl(
            f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.image_key}"
        )
