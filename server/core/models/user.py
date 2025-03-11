import enum
import typing

from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy import (
    LargeBinary,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import RecordModel

# from .content import  Content
if typing.TYPE_CHECKING:
    from .content import Content


class ImageStatus(enum.Enum):
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"


class AuthType(str, enum.Enum):
    local = "local"
    google = "google"


class User(RecordModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, unique=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    password_salt: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    profile_photo_key: Mapped[str] = mapped_column(String(100), nullable=True)
    auth_type: Mapped[AuthType] = mapped_column(
        SAEnum(AuthType), nullable=False, default=AuthType.local
    )
    contents: Mapped["Content"] = relationship("Content", back_populates="user")
