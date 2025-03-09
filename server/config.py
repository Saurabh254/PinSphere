__all__ = ["settings"]

from typing import Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    redis_dsn: RedisDsn
    ALGORITHM: str
    AUTH_SECRET: str
    AWS_STORAGE_BUCKET_NAME: str
    AWS_REGION: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_ACCESS_KEY_ID: str
    AWS_SESSION_TOKEN: str
    AWS_SIGNATURE_VERSION: str
    REFRESH_TOKEN_EXPIRATION_SECONDS: int
    AWS_ENDPOINT_URL: str
    RABBIT_MQ_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def get_database_dsn(self, driver: Literal["asyncpg", "psycopg"]) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+{driver}://postgres:postgres@localhost:5432/pin_sphere"
        )


settings = Settings()  # type: ignore
