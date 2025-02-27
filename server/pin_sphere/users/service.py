import uuid

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core import storage
from core.authflow.service import hash_password
from core.models import Content, User
from core.types import FileContentType

from ..base_exception import ServerError
from .schemas import UserCreate, UserUpdate


# Service to fetch a single users by username
async def get_user(db: AsyncSession, username: str):
    try:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalars().one()
    except NoResultFound:
        return None


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
async def update_user(db: AsyncSession, user: User, user_update: UserUpdate):
    # get the current users

    # check if the given username exists or not
    result = await db.execute(
        select(User).filter(User.username == user_update.username)
    )
    existing_user_with_given_username = result.scalars().one_or_none()
    if existing_user_with_given_username:
        raise HTTPException(status_code=400, detail="Username already exists")
    update_data = user_update.model_dump(exclude_unset=True)
    # TODO: Fix updating of username
    # AsOfNow username is the foreign key in tables. so it's a pain to do this job.
    # instead we'll come with an efficient solution.

    if "username" in update_data.keys():
        return

    # Update only the fields that are provided
    for key, value in update_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)  # Refresh to return the updated users
    return user


async def move_assets_to_new_User(
    db: AsyncSession, user: User, new_username: str
) -> User:
    # First check if the new username already exists
    existing_user = await db.execute(select(User).where(User.username == new_username))
    existing_user = existing_user.scalars().first()

    if existing_user:
        raise ValueError(f"Username '{new_username}' already exists")

    # Store old username for reference
    old_username = user.username

    # Create a temporary intermediary username that won't exist in the system
    temp_username = f"temp_{uuid.uuid4().hex[:10]}_{old_username}"

    # Step 1: Update all content to use the temporary username
    await db.execute(
        update(Content)
        .where(Content.username == old_username)
        .values(username=temp_username)
    )

    # Step 2: Update the user to have the temporary username
    user.username = temp_username
    await db.flush()

    # Step 3: Update the user to have the final new username
    user.username = new_username
    await db.flush()

    # Step 4: Update all content from temp username to the new username
    await db.execute(
        update(Content)
        .where(Content.username == temp_username)
        .values(username=new_username)
    )

    # Refresh user to get latest data
    await db.refresh(user)

    return user


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


def get_user_profile_key(username: str, ext: FileContentType) -> str:
    return f"profile/{username}/{uuid.uuid4()}.{ext.name.casefold()}"


def get_upload_url(user: User, ext: FileContentType):
    content_key = get_user_profile_key(user.username, ext)
    res = storage.create_presigned_post(content_key, ext)
    if not res:
        raise ServerError(status_code=500, message="Failed to create presigned URL")
    return res
