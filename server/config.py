__all__ = ["settings"]


from typing import Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_dsn: RedisDsn = RedisDsn(
        "redis://localhost:6379/0",
    )
    ALGORITHM: str = "HS256"
    AUTH_SECRET: str = (
        "159cdf30c1cee803eec9dc63bb16c1b2882c4354aa2eb6a34a46ed50775d94ad"
    )
    AWS_STORAGE_BUCKET_NAME: str = "pinsphere"
    AWS_REGION: str = "us-east-1"
    AWS_SECRET_ACCESS_KEY: str = "lzBdlQOBsAREMnmBD0LaUOm6NUTZO5i5awjf6Bkw"
    AWS_ACCESS_KEY_ID: str = "uGPRISlXZ7rBkB3PahjU"
    AWS_SESSION_TOKEN: str = "saurabh_prod"
    AWS_SIGNATURE_VERSION: str = "s3v4"
    AWS_ENDPOINT_URL: str = "http://localhost:9000"

    def get_database_dsn(self, driver: Literal["asyncpg", "psycopg"]) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+{driver}://postgres:postgres@localhost:5432/pin_sphere"
        )

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore
