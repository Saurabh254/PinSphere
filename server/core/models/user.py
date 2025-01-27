import enum
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import (
    Boolean,
    ForeignKey,
    LargeBinary,
    String,
    UUID as SA_UUID,
    Enum as saEnum,
)
from core.database.base_model import TimeStampModel, RecordModel


class ImageStatus(enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class User(TimeStampModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(50), nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    password_salt: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)


class UserPhotos(RecordModel):
    __tablename__ = "user_photos"
    user_id: Mapped[UUID] = mapped_column(
        SA_UUID, ForeignKey("users.id"), nullable=False
    )
    image_key: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[ImageStatus] = mapped_column(
        saEnum("PROCESSED", "PROCESSING"),
        nullable=False,
        default=ImageStatus.PROCESSING,
    )
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    blurhash: Mapped[str] = mapped_column(String(50), nullable=True)
