import enum
from typing import Dict

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config import settings
from core.database.base_model import RecordModel
# from .user import User
import typing

if typing.TYPE_CHECKING:
    from .user import User

class ContentProcessingStatus(enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class Content(RecordModel):
    __tablename__ = "contents"
    username: Mapped[str] = mapped_column(
        String(50), ForeignKey("users.username"), nullable=False
    )
    blurhash: Mapped[str] = mapped_column(String(50), nullable=True)
    content_key: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[ContentProcessingStatus] = mapped_column(
        SAEnum(ContentProcessingStatus, name="content_processing_enum"), nullable=False
    )
    likes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    description: Mapped[str] = mapped_column(String, nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    _metadata: Mapped[Dict[str, str | int | bool]] = mapped_column(JSONB, nullable=True)
    user: Mapped["User"] = relationship('User', back_populates='contents')
    @hybrid_property
    def url(self):
        return f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.image_key}"
