from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Base class for all models
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # Makes this class abstract and not mapped to a table

    # Common fields
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Optionally add common methods
    def as_dict(self):
        """Convert model instance to dictionary for easy serialization."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
