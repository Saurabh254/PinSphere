import io
import uuid
from typing import BinaryIO

import blurhash  # type: ignore
import boto3
from PIL import Image
from typing_extensions import Tuple

from config import settings
from core.types import FileContentType


def get_content_key(username: str, ext: FileContentType) -> str:
    """
    Generate a unique content key for the given username and extension.

    Args:
        username (str): The username of the user.
        ext (str): The file extension of the content.

    Returns:
        str: The generated content key
    """
    return f"content/{username}/{uuid.uuid4()}.{ext.name.casefold()}"


# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.AWS_ENDPOINT_URL,
)


def get_content(content_key: str) -> BinaryIO:
    """
    Fetches content from AWS S3 storage using the provided content key.

    Args:
        content_key (str): The key of the content to retrieve from S3.

    Returns:
        BinaryIO: A binary stream of the content retrieved from S3.
    """
    return io.BytesIO(
        s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=content_key)[
            "Body"
        ].read()
    )  # type: ignore


def retrieve_blurhash_by_content_key(content_key: str) -> str:
    image = Image.open(get_content(content_key)).convert("RGB")
    return blurhash.encode(image, x_components=4, y_components=4)  # type:ignore


def retrieve_blurhash_and_metadata(content_key: str) -> Tuple[str, dict[str, int]]:
    image = Image.open(get_content(content_key)).convert("RGB")
    return blurhash.encode(image, x_components=4, y_components=4), {  # type: ignore
        "width": image.size[0],
        "height": image.size[1],
    }
