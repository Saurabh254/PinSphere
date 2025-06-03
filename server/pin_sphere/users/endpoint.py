from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.authflow import auth
from core.database.session_manager import get_async_session
from core.models import User
from core.types import FileContentType

from . import filters, schemas, service

# Create an API router for users-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["Account Operations"],
)


@router.get(
    "/me",
    response_model=schemas.UserResponse,
    summary="Get current user profile",
    description="Retrieve the profile information of the currently authenticated user.",
    tags=["Account Operations"],
)
async def get_me(
    current_user: User = Depends(auth.get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get current authenticated user's profile"""
    return await service.get_user(session, current_user.username)


@router.get(
    "",
    response_model=list[schemas.UserResponse],
    summary="List all users",
    description="Fetch a paginated list of all users in the system.",
    tags=["Account Operations"],
    dependencies=[Depends(auth.get_current_user)],
)
async def read_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Fetch a list of users with optional pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    """
    # Fetch users with pagination
    users = await service.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/check-username/{username}",
    summary="Check username availability",
    description="Verify if a username is available for registration.",
    tags=["Account Operations"],
    dependencies=[Depends(auth.get_current_user)],
)
async def check_username_availability(
    username: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Check if the provided username is available for registration.

    - **username**: The username to check for availability

    Returns success message if available, otherwise raises 400 error.
    """
    # Check if username already exists
    existing_user = await service.get_user_by_username(db, username=username)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return {"message": "Username is available"}


@router.delete(
    "/{username}",
    response_model=schemas.UserResponse,
    summary="Delete user account",
    description="Delete a user account by username. Returns the deleted user information.",
    tags=["Account Operations"],
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_account(
    username: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Delete a user account by their username.

    - **username**: The username of the user to delete

    Returns the deleted user data or 404 if user not found.
    """
    # Attempt to delete user
    user = await service.delete_user(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "/upload_url",
    summary="Get profile photo upload URL",
    description="Generate a pre-signed URL for uploading profile photos. Supports PNG and JPEG formats.",
    tags=["Account Operations"],
)
async def retrieve_upload_url(
    ext: Literal["image/png", "image/jpeg"],
    current_user: User = Depends(auth.get_current_user),
):
    """
    Generate upload URL for profile photo.

    - **ext**: Image format (image/png or image/jpeg)
    """
    # Convert extension and generate upload URL
    ext_ = FileContentType(ext)
    return service.get_upload_url(current_user, ext=ext_)


@router.get(
    "/settings",
    summary="Get user settings",
    description="Retrieve the current user's account settings and preferences.",
    tags=["Account Operations"],
    response_model=filters.SettingsFilter,
)
async def get_settings(
    current_user: User = Depends(auth.get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get current user's settings"""
    return await service.get_settings(session, current_user)


@router.put(
    "/settings",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update user settings",
    description="Update the current user's account settings and preferences.",
)
async def update_settings(
    current_user: User = Depends(auth.get_current_user),
    settings: filters.SettingsFilter = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    """Update current user's settings"""
    await service.update_settings(current_user, settings, session)


@router.get(
    "/{username}",
    response_model=schemas.UserResponse,
    summary="Get user by username",
    description="Retrieve a specific user's profile information by their username.",
    tags=["Account Operations"],
)
async def read_user(
    username: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Fetch a single user by their unique username.

    - **username**: The username of the user to retrieve

    Returns user data or 404 if user not found.
    """
    # Fetch user by username
    user = await service.get_user(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put(
    "",
    response_model=schemas.UserResponse,
    summary="Update current user",
    description="Update the current authenticated user's profile information (name, email, etc.).",
    tags=["Account Operations"],
)
async def update_existing_user(
    user_update: schemas.UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth.get_current_user),
):
    """
    Update the current user's profile information.

    - **user_update**: JSON payload containing the fields to update (name, email, etc.)

    Returns updated user data or 404 if user not found.
    """
    # Update current user's information
    user = await service.update_user(db, current_user, user_update=user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Note: Duplicate delete endpoint - consider removing one of the delete methods
@router.delete(
    "/{username}",
    response_model=schemas.UserResponse,
    summary="Delete user by username",
    description="Delete a user account by username. This is a duplicate endpoint.",
    tags=["Account Operations"],
    dependencies=[Depends(auth.get_current_user)],
)
async def delete_existing_user(
    username: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Delete a user by their unique username.

    - **username**: The username of the user to delete

    Returns deleted user data or 404 if user not found.
    """
    # Delete user by username
    user = await service.delete_user(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
