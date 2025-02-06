import enum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy import Enum as SAEnum
from config import settings
from core.database.base_model import RecordModel


class ImageProcessingStatus(enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class Images(RecordModel):
    __tablename__ = "images"
    username: Mapped[str] = mapped_column(
        String(50), ForeignKey("users.username"), nullable=False
    )
    blurhash: Mapped[str] = mapped_column(String(50), nullable=True)
    image_key: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[ImageProcessingStatus] = mapped_column(
        SAEnum(ImageProcessingStatus, name="image_processing_enum"), nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    @hybrid_property
    def url(self):
        return f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.image_key}"
