# type: ignore


from celery_app import app
from core.boto3_client import s3_client
from core.database.session_manager import get_sync_session
from core.models.content import ContentProcessingStatus
from logging_conf import log
from pin_sphere.content import service
from pin_sphere.content.utils import (
    retrieve_blurhash_and_metadata,
)


@app.task
def generate_blurhash(image_id: str, image_key: str):
    """Compresses an image from S3 and uploads it back.

    Args:
        image_id (str): The ID of the image.
        image_key: S3 object key (path in bucket).
    """
    try:
        with next(get_sync_session()) as session:
            blurhash_encoding, metadata = retrieve_blurhash_and_metadata(image_key)

            service.update_content(
                image_id,
                session,
                blurhash=blurhash_encoding,
                _metadata=metadata,
                status=ContentProcessingStatus.PROCESSED,
            )
        log.debug(
            "Blurhash successfully created.",
            extra={
                "image_id": image_id,
                "blurhash_encoding": blurhash_encoding,
                "image_key": image_key,
            },
        )
    except s3_client.exceptions.NoSuchKey:
        log.error(f"Image not found with image id [{image_key}]")
    except Exception as e:
        print(f"An error occurred: {e}")
