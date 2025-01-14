from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema for creating a user
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Schema for updating a user (optional fields)
class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]

# Schema for returning user information
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    # Config class to allow ORM models to be serialized
    class Config:
        orm_mode = True
