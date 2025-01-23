#
# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import List
# from .schemas import ImageCreate, ImageResponse
# from .service import ImageService
# from .dependencies import get_db
#
# router = APIRouter(prefix="/images", tags=["images"])
# image_service = ImageService(s3_bucket="your-bucket-name")
#
# @router.post("/", response_model=ImageResponse)
# async def upload_image(
#     file: UploadFile = File(...),
#     user_id: UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Upload a new image for a user
#     """
#     return await image_service.upload_image(file, user_id, db)
#
# @router.get("/{image_id}", response_model=ImageResponse)
# async def get_image(
#     image_id: UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Get image details by ID
#     """
#     image = await image_service.get_image(image_id, db)
#     if not image:
#         raise HTTPException(status_code=404, detail="Image not found")
#     return image
#
# @router.delete("/{image_id}")
# async def delete_image(
#     image_id: UUID,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Delete an image by ID
#     """
#     success = await image_service.delete_image(image_id, db)
#     if not success:
#         raise HTTPException(status_code=404, detail="Image not found")
#     return {"status": "success"}
