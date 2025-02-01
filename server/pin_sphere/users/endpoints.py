from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.session_manager import get_async_session
from core.models import User
from pin_sphere.users.service import get_user_by_email, get_user_by_username
from .schemas import UserCreate, UserUpdate, UserResponse
from .service import get_user, get_users, create_user, update_user, delete_user
from core.authflow import auth

# Create an API router for users-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["Account Operations"],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    tags=["Account Operations"],
)
async def get_me(
    current_user: User = Depends(auth.get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await get_user(session, current_user.username)


# Fetch all users with optional pagination
@router.get(
    "",
    response_model=list[UserResponse],
    summary="Fetch all users",
    tags=["Account Operations"],
)
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Fetch a list of users with optional pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    """
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/check-username/{username}",
    summary="Check if a username is available",
    tags=["Account Operations"],
)
async def check_username_availability(
    username: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Check if the provided username is available for registration.

    - **username**: The username to check.
    """
    existing_user = await get_user_by_username(db, username=username)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return {"message": "Username is available"}


# Account deletion route
@router.delete(
    "/delete/{username}",
    response_model=UserResponse,
    summary="Delete an account by username",
    tags=["Account Operations"],
)
async def delete_account(
    username: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Delete the users account by their username.

    - **username**: The username of the users to delete.
    """
    user = await delete_user(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Fetch a specific users by username
@router.get(
    "/{username}",
    response_model=UserResponse,
    summary="Fetch a users by username",
    tags=["Account Operations"],
)
async def read_user(
    username: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Fetch a single users by their unique username.

    - **username**: The username of the users to retrieve.
    """
    user = await get_user(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Create a new users
@router.post(
    "",
    response_model=UserResponse,
    summary="Create a new users",
    tags=["Account Operations"],
)
async def create_new_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Create a new users with the provided details.

    - **users**: JSON payload containing users details (name, email, password).
    """
    # Additional validation (e.g., checking for existing email or username) could go here.
    existing_user_by_email = await get_user_by_email(db, email=user.email)
    existing_user_by_username = await get_user_by_username(db, username=user.username)

    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    return await create_user(db, user)


# Update an existing users
@router.put(
    "/{username}",
    response_model=UserResponse,
    summary="Update a users",
    tags=["Account Operations"],
)
async def update_existing_user(
    username: str,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Update an existing users by their unique username.

    - **username**: The username of the users to update.
    - **user_update**: JSON payload containing the fields to update (name, email).
    """
    user = await update_user(db, username=username, user_update=user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Delete a users by username
@router.delete(
    "/{username}",
    response_model=UserResponse,
    summary="Delete a users",
    tags=["Account Operations"],
)
async def delete_existing_user(
    username: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Delete a users by their unique username.

    - **username**: The username of the users to delete.
    """
    user = await delete_user(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
