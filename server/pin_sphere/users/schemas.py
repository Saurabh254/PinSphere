from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, SecretStr, computed_field

from config import settings


# Schema for creating a users
class UserCreate(BaseModel):
    username: str  # Username as the unique identifier
    email: EmailStr
    password: SecretStr


# Schema for updating a users (optional fields)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None) # Allow username to be updated, if needed
    name: Optional[str]= Field(None)
    email: Optional[EmailStr]= Field(None)
    profile_photo_key: Optional[str]= Field(None, alias="image_key")


# Schema for returning users information
class UserResponse(BaseModel):
    username: str  # Replaced `id` with `username`
    name: str
    email: EmailStr
    created_at: datetime
    profile_photo_key: str|None = Field(None, exclude=True)

    @computed_field
    def url(self) -> HttpUrl | None:
        if self.profile_photo_key:
            return HttpUrl(
                f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{self.profile_photo_key}"
            )
        return None
