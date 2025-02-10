import io
import uuid
from typing import BinaryIO

import blurhash  # type: ignore
import boto3
from PIL import Image
from typing_extensions import Tuple

from config import settings
from core.types import FileContentType


def get_image_key(username: str, ext: FileContentType) -> str:
    """
    Generate a unique image key for the given username and extension.

    Args:
        username (str): The username of the user.
        ext (str): The file extension of the image.

    Returns:
        str: The generated image key
    """
    return f"images/{username}/{uuid.uuid4()}.{ext.name.casefold()}"


# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.AWS_ENDPOINT_URL,
)


def get_image(image_key: str) -> BinaryIO:
    """
    Fetches an image from AWS S3 storage using the provided image key.

    Args:
        image_key (str): The key of the image to retrieve from S3.

    Returns:
        BinaryIO: A binary stream of the image retrieved from S3.
    """
    return io.BytesIO(
        s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=image_key)[
            "Body"
        ].read()
    )  # type: ignore


def retrieve_blurhash_by_image_key(image_key: str) -> str:
    image = Image.open(get_image(image_key)).convert("RGB")
    return blurhash.encode(image, x_components=4, y_components=4)  # type:ignore


def retrieve_blurhash_and_metadata(image_key: str) -> Tuple[str, dict[str, int]]:
    image = Image.open(get_image(image_key)).convert("RGB")
    return blurhash.encode(image, x_components=4, y_components=4), {  # type: ignore
        "width": image.size[0],
        "height": image.size[1],
    }
