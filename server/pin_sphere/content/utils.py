import io
import logging
import uuid
from typing import BinaryIO

import blurhash  # type: ignore
import boto3
from PIL import Image
from typing_extensions import Tuple

from config import settings
from core.types import FileContentType
from pin_sphere.content.exceptions import ContentNotFoundError

log = logging.getLogger(__name__)


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


def get_content(content_key: str) -> Tuple[BinaryIO, str]:
    """
    Fetches content from AWS S3 storage using the provided content key.

    Args:
        content_key (str): The key of the content to retrieve from S3.

    Returns:
        BinaryIO: A binary stream of the content retrieved from S3.
    """
    try:
        s3_object = s3_client.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=content_key
        )
        response = io.BytesIO(s3_object["Body"].read())  # type: ignore
        return response, s3_object["ContentType"]  # type: ignore
    except Exception as e:
        log.error(e)
        raise e


def retrieve_blurhash_by_content_key(content_key: str) -> str:
    image, content_type = get_content(content_key)
    image = Image.open(image).convert("RGB")
    return (
        blurhash.encode(image, x_components=4, y_components=4),  # type:ignore
        content_type,
    )


def retrieve_blurhash_and_metadata(
    content_key: str,
) -> Tuple[str, dict[str, int | str]]:
    image, content_type = get_content(content_key)
    image = Image.open(image).convert("RGB")
    return blurhash.encode(image, x_components=4, y_components=4), {  # type: ignore
        "width": image.size[0],
        "height": image.size[1],
        "content_type": content_type,
    }


def get_content_type_from_s3(content_key: str) -> str:
    try:
        return s3_client.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=content_key
        )["ContentType"]
    except s3_client.exceptions.NoSuchKey as e:
        raise ContentNotFoundError(message=str(e))
    except Exception as e:
        log.error(e)
        raise e
