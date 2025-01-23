# import boto3
# from uuid import UUID
# from fastapi import UploadFile
# from sqlalchemy.ext.asyncio import AsyncSession
# from .models import UserPhotos
#
#
# class ImageService:
#     def __init__(self, s3_bucket: str):
#         self.s3_client = boto3.client("s3")
#         self.bucket = s3_bucket
#
#     async def upload_image(
#         self, file: UploadFile, user_id: UUID, db: AsyncSession
#     ) -> UserPhotos:
#         # Generate unique S3 key
#         image_key = f"users/{user_id}/images/{file.filename}"
#
#         # Upload to S3
#         await self.s3_client.upload_fileobj(file.file, self.bucket, image_key)
#
#         # Create database record
#         photo = UserPhotos(
#             user_id=user_id,
#             image_key=image_key,
#             status=ImageStatus.PROCESSING,
#             deleted=False,
#         )
#
#         db.add(photo)
#         await db.commit()
#         await db.refresh(photo)
#         return photo
#
#     async def get_image(self, image_id: UUID, db: AsyncSession) -> Optional[UserPhotos]:
#         return await db.get(UserPhotos, image_id)
#
#     async def delete_image(self, image_id: UUID, db: AsyncSession) -> bool:
#         photo = await self.get_image(image_id, db)
#         if not photo:
#             return False
#
#         # Soft delete in database
#         photo.deleted = True
#         await db.commit()
#
#         # Delete from S3
#         await self.s3_client.delete_object(Bucket=self.bucket, Key=photo.image_key)
#         return True
