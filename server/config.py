__all__ = ["settings"]


from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_dsn: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/pin_sphere"
    )
    redis_dsn: RedisDsn = RedisDsn(
        "redis://localhost:6379/0",
    )
    ALGORITHM: str = "HS256"
    AUTH_SECRET: str = (
        "159cdf30c1cee803eec9dc63bb16c1b2882c4354aa2eb6a34a46ed50775d94ad"
    )

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
