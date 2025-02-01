# from uuid import UUID
#
# from celery import Celery
# from blurhash import encode
# from PIL import Image
# from io import BytesIO
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from core.dependency_injector import Inject, inject_asyncpg_session
# from core.models.user import ImageStatus
#
# celery = Celery("tasks", broker="redis://localhost:6379/0")
#
#
# @celery.task
# @inject_asyncpg_session
# async def process_image(image_id: UUID, session: AsyncSession = Inject()):
#     """
#     Process uploaded image to generate blurhash
#     """
#     photo = await session.get(UserPhotos, image_id)
#
#     if not photo:
#         return
#
#     # Download image from S3
#
#
#     # Generate blurhash
#     blurhash = encode(image)
#
#     # Update database
#     photo.blurhash = blurhash
#     photo.status = ImageStatus.PROCESSED
#     await session.commit()
