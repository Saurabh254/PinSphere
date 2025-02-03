__all__ = ["router"]

from pin_sphere.users import endpoints as user_endpoints

from fastapi import APIRouter
from pin_sphere.auth import endpoint as auth_endpoint
from pin_sphere.images import endpoint as image_endpoint

router = APIRouter(prefix="/api/v1")


router.include_router(user_endpoints.router)
router.include_router(auth_endpoint.router)
router.include_router(image_endpoint.router)
