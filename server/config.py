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
    AWS_SECRET_ACCESS_KEY: str = "wx0AHiNqPnJbiPTj55Fz2fR81EU3jdpPjyAPeZ6y"
    AWS_ACCESS_KEY_ID: str = "Q9LPDloAiLJODVTEinQQ"
    AWS_SESSION_TOKEN: str = "saurabh_prod"
    AWS_SIGNATURE_VERSION: str = "s3v4"
    REFRESH_TOKEN_EXPIRATION_SECONDS: int = 60 * 60 * 24 * 15  # 15 days
    AWS_ENDPOINT_URL: str = "https://minio.saurabhvishwakarma.in"
    RABBIT_MQ_URL: str = "redis://localhost:6379/0"

    def get_database_dsn(self, driver: Literal["asyncpg", "psycopg"]) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+{driver}://postgres:postgres@localhost:5432/pin_sphere"
        )

    class ConfigDict:
        env_file = ".env"


settings = Settings()  # type: ignore
