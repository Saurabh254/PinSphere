import enum
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Boolean, ForeignKey, String, UUID as SA_UUID, Enum as saEnum
from core.database.base_model import BaseModel


class ImageStatus(enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class User(BaseModel):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(SA_UUID, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(50), nullable=False)
    password_salt: Mapped[str] = mapped_column(String(50), nullable=False)


class UserPhotos(BaseModel):
    __tablename__ = "user_photos"
    id: Mapped[UUID] = mapped_column(SA_UUID, primary_key=True)
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
