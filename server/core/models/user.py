import enum

from sqlalchemy import (
    LargeBinary,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from core.database.base_model import TimeStampModel


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
