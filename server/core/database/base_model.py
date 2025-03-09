import uuid

from pydantic import UUID4
from sqlalchemy import UUID, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

# Base class for all models
Base = declarative_base()


class TimeStampModel(Base):
    __abstract__ = True

    # Common fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    # Optionally add common methods
    def as_dict(self):
        """Convert model instance to dictionary for easy serialization."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class RecordModel(TimeStampModel):
    __abstract__ = True

    # Common fields
    id: Mapped[UUID4] = mapped_column(
        UUID, primary_key=True, index=True, default=lambda: uuid.uuid4()
    )
