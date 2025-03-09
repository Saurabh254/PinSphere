__all__ = ["get_async_session", "get_sync_session"]

from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from config import settings

async_engine: AsyncEngine = create_async_engine(
    str(settings.get_database_dsn("asyncpg")), echo=True
)
sync_engine = create_engine(str(settings.get_database_dsn("psycopg")), echo=False)

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)
sync_session = sessionmaker(bind=sync_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Asynchronous generator function that provides an asynchronous session.

    Yields:
        AsyncSession: An instance of an asynchronous session.
    """
    async with async_session() as session:
        yield session


def get_sync_session():
    """
    Provides a synchronous database session generator.

    Yields:
        Session: A synchronous database session.
    """
    with sync_session() as session:
        yield session
