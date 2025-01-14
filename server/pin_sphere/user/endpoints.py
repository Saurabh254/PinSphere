from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db  # Async database session dependency
from schemas import UserCreate, UserUpdate, UserResponse
from service import get_user, get_users, create_user, update_user, delete_user

# Create an API router for user-related endpoints
router = APIRouter(
    prefix='/user',
    tags=['user'], 
)

# Fetch all users with optional pagination
@router.get("/users", response_model=list[UserResponse], summary="Fetch all users", tags=["Users"])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Fetch a list of users with optional pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 10)
    """
    users = await get_users(db, skip=skip, limit=limit)
    return users

# Fetch a specific user by ID
@router.get("/users/{user_id}", response_model=UserResponse, summary="Fetch a user by ID", tags=["Users"])
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetch a single user by their unique ID.

    - **user_id**: The ID of the user to retrieve.
    """
    user = await get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new user
@router.post("/users", response_model=UserResponse, summary="Create a new user", tags=["Users"])
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new user with the provided details.

    - **user**: JSON payload containing user details (name, email, password).
    """
    # Additional validation (e.g., checking for existing email) could go here.
    existing_user = await db.execute(select(User).filter(User.email == user.email))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    return await create_user(db, user)

# Update an existing user
@router.put("/users/{user_id}", response_model=UserResponse, summary="Update a user", tags=["Users"])
async def update_existing_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update an existing user by their unique ID.

    - **user_id**: The ID of the user to update.
    - **user_update**: JSON payload containing the fields to update (name, email).
    """
    user = await update_user(db, user_id=user_id, user_update=user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete a user by ID
@router.delete("/users/{user_id}", response_model=UserResponse, summary="Delete a user", tags=["Users"])
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a user by their unique ID.

    - **user_id**: The ID of the user to delete.
    """
    user = await delete_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
