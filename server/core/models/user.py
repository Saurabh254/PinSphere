import enum

from sqlalchemy import (
    LargeBinary,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import RecordModel, TimeStampModel
# from .content import  Content

class ImageStatus(enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class User(RecordModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), nullable=False,index=True, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    password_salt: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    profile_photo_key: Mapped[str] = mapped_column(String(100), nullable=True)
    contents: Mapped["Content"] = relationship("Content", back_populates="user")
