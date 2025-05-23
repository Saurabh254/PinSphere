import io
import logging
from typing import BinaryIO

import boto3  # type: ignore
from botocore.exceptions import BotoCoreError, ClientError  # type: ignore
from PIL import Image
from PIL.ImageFile import ImageFile

from config import settings

from .types import FileContentType

log = logging.getLogger(__name__)
s3_client = boto3.client(  # type: ignore
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=settings.AWS_ENDPOINT_URL,
    verify=False,
)


def get_image(s3_key: str) -> ImageFile:
    """
    Fetches an image from S3, extracts its bytes, and gets contextual information using LangChain Ollama (LLaMA 3.2).

    Args:
        s3_key (str): Key (path) of the image in S3.

    Returns:
        str: Contextual description of the image.
    """
    # Initialize Boto3 S3 client

    # Fetch image from S3

    response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    image_data = response["Body"].read()

    # Convert image to a format suitable for processing
    return Image.open(io.BytesIO(image_data))


def upload_content(
    file: BinaryIO,
    file_name: str,
    content_type: FileContentType,
) -> str | None:
    """Uploads an image to S3 and returns its URL."""
    try:
        s3_client.upload_fileobj(  # type: ignore
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            file_name,
            ExtraArgs={"ContentType": content_type},
        )
        return f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_name}"
    except (BotoCoreError, ClientError) as e:
        log.error(f"Error uploading image: {e}")
        return None


def get_image_url(key: str) -> str:
    """Returns the image URL given its key."""
    return f"{settings.AWS_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{key}"


def create_presigned_get(object_name: str, expiration: int = 3600) -> str | None:
    """Generate a presigned URL to share an S3 object

    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3_client.generate_presigned_url(  # type: ignore
            "get_object",  # type: ignore
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError:
        # log.error(e)
        return None
    # The response contains the presigned URL
    return response  # type: ignore


def create_presigned_post(
    object_name: str,
    content_type: FileContentType,
    file_size: int = 500 * 1024,
    expiration: int = 3600,
) -> dict[str, str] | None:
    """Generate a presigned URL S3 POST request to upload a file

    :param object_name: string
    :param file_size: size of the file in bytes
    :param content_type: mime type of the file
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with url and fields, or None if error
    """
    try:
        conditions = [
            #     ['content-length-range', 1, file_size],  # Add buffer for metadata
            {"bucket": settings.AWS_STORAGE_BUCKET_NAME},
            {"key": object_name},
            {
                "Content-Type": content_type.value,
            },
        ]

        response = s3_client.generate_presigned_post(  # type: ignore
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=object_name,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
        return response  # type: ignore
    except ClientError as e:
        log.error(f"Error generating presigned URL: {e}")
        return None


#

if __name__ == "__main__":
    print(create_presigned_post("okkkk", FileContentType.PNG))
