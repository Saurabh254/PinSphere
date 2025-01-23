# from celery import Celery
# from blurhash import encode
# from PIL import Image
# from io import BytesIO
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# celery = Celery("tasks", broker="redis://localhost:6379/0")
#
#
# @celery.task
# async def process_image(image_id: UUID, db: AsyncSession = ...):
#     """
#     Process uploaded image to generate blurhash
#     """
#     db = SessionLocal()
#     photo = await db.get(UserPhotos, image_id)
#
#     if not photo:
#         return
#
#     # Download image from S3
#     response = s3_client.get_object(Bucket=BUCKET_NAME, Key=photo.image_key)
#     image = Image.open(BytesIO(response["Body"].read()))
#
#     # Generate blurhash
#     blurhash = encode(image)
#
#     # Update database
#     photo.blurhash = blurhash
#     photo.status = ImageStatus.PROCESSED
#     await db.commit()
