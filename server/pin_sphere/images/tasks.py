# type: ignore
import os


import boto3
import sys


import io
from PIL import Image

from celery_app import app

sys.path.append(os.getcwd())
from config import settings

sys.path.remove(os.getcwd())


# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


@app.task
def compress_image_s3(object_key: str, quality: int = 60):
    """Compresses an image from S3 and uploads it back.

    Args:
        object_key: S3 object key (path in bucket).
        quality: Compression quality (0-100, higher is better) default to 60.
    """
    try:
        # Download image from S3
        response = s3_client.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=object_key
        )
        img = Image.open(io.BytesIO(response["Body"].read()))

        # Compress image
        compressed_image = io.BytesIO()
        img.save(compressed_image, format=img.format, optimize=True, quality=quality)
        compressed_image.seek(0)

        # Generate new object key
        filename, ext = object_key.rsplit(".", 1)
        compressed_key = f"{filename}_compressed.{ext}"

        # Upload compressed image back to S3
        s3_client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=compressed_key,
            Body=compressed_image,
            ContentType=response["ContentType"],
        )

    except s3_client.exceptions.NoSuchKey:
        print(f"Error: Image file not found in S3: {object_key}")
    except Exception as e:
        print(f"An error occurred: {e}")
