from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from models import User  # Assuming `User` SQLAlchemy model is defined elsewhere
from schemas import UserCreate, UserUpdate

# Service to fetch a single user by ID
async def get_user(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().one()
    except NoResultFound:
        return None

# Service to fetch multiple users with pagination
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

# Service to create a new user
async def create_user(db: AsyncSession, user: UserCreate):
    # Add password hashing logic here
    hashed_password = user.password
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Refresh to get the newly created user with ID
    return new_user

# Service to update an existing user
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        return None

    # Update only the fields that are provided
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)  # Refresh to return the updated user
    return db_user

# Service to delete a user by ID
async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        return None

    await db.delete(db_user)
    await db.commit()
    return db_user
