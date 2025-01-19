from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


# Schema for creating a users
class UserCreate(BaseModel):
    username: str  # Username as the unique identifier
    email: EmailStr
    password: str


# Schema for updating a users (optional fields)
class UserUpdate(BaseModel):
    username: Optional[str]  # Allow username to be updated, if needed
    name: Optional[str]
    email: Optional[EmailStr]


# Schema for returning users information
class UserResponse(BaseModel):
    username: str  # Replaced `id` with `username`
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    # Config class to allow ORM models to be serialized
    class Config:
        from_attributes = True
