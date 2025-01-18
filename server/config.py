__all__ = ["settings"]


from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_dsn: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://saurabh254:prod_123@localhost:5432/pin_sphere"
    )
    redis_dsn: RedisDsn = RedisDsn(
        "redis://localhost:6379/0",
    )

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
