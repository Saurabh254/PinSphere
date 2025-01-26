__all__ = ["router"]

from pin_sphere.users import endpoints

from fastapi import APIRouter
from pin_sphere.auth import endpoint as auth_endpoint

router = APIRouter(prefix="/api/v1")


router.include_router(endpoints.router)
router.include_router(auth_endpoint.router)
