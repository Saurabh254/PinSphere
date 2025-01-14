__all__ = ['settings']


from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_dsn: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
    redis_dsn: RedisDsn = Field(
        'redis://localhost:6379/0',

    )
    class Config:
        env_file = ".env"

settings = Settings()
