import secrets
import hashlib
import os

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from core.authflow.service import hash_password
from core.models import User
from .schemas import UserCreate, UserUpdate


# Service to fetch a single users by username
async def get_user(db: AsyncSession, username: str):
    try:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().one()
    except NoResultFound:
        return None


async def verify_user(session: AsyncSession, username: str, password: str):
    user = await get_user(session, username)




# Service to fetch a users by email
async def get_user_by_email(db: AsyncSession, email: EmailStr):
    try:
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalars().one()
    except NoResultFound:
        return None


# Service to fetch multiple users with pagination
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    print("this is db: ", db)
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


# Service to create a new users
async def create_user(db: AsyncSession, user_data: UserCreate):
    # Add password hashing logic here
    hashed_salt, hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        name=user_data.username,
        email=str(user_data.email),
        password=hashed_password,
        password_salt=hashed_salt,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Refresh to get the newly created users
    return new_user


# Service to update an existing users
async def update_user(db: AsyncSession, username: str, user_update: UserUpdate):
    # get the current users
    result = await db.execute(select(User).filter(User.username == username))
    db_user = result.scalars().first()
    if not db_user:
        return None
    del result
    # check if the given username exists or not
    result = await db.execute(
        select(User).filter(User.username == user_update.username)
    )
    existing_user_with_given_username = result.scalars().one()
    if existing_user_with_given_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    # Update only the fields that are provided
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)  # Refresh to return the updated users
    return db_user


# Service to delete a users by username
async def delete_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    db_user = result.scalars().first()
    if not db_user:
        return None

    await db.delete(db_user)
    await db.commit()
    return db_user


# Service to fetch a users by username
async def get_user_by_username(db: AsyncSession, username: str):
    try:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().first()
    except NoResultFound:
        return None
