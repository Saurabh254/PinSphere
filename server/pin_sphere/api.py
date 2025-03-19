__all__ = ["router"]

from fastapi import APIRouter

from pin_sphere.auth import endpoint as auth_endpoint
from pin_sphere.content import endpoint as content_endpoint
from pin_sphere.users import endpoint as user_endpoints
from pin_sphere.comments import endpoint as comments_endpoint
router = APIRouter(prefix="/api/v1")


router.include_router(user_endpoints.router)
router.include_router(auth_endpoint.router)
router.include_router(content_endpoint.router)
router.include_router(comments_endpoint.router)
