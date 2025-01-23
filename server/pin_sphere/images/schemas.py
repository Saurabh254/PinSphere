# from typing import Optional
# from uuid import UUID
# from pydantic import BaseModel
# from enum import Enum
#
#
# class ImageStatus(str, Enum):
#     PROCESSED = "PROCESSED"
#     PROCESSING = "PROCESSING"
#
#
# class ImageCreate(BaseModel):
#     user_id: UUID
#
#
# class ImageResponse(BaseModel):
#     id: UUID
#     user_id: UUID
#     image_key: str
#     status: ImageStatus
#     blurhash: Optional[str]
