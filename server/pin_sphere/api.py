__all__ = ["router"]

from pin_sphere.users import endpoints

from fastapi import APIRouter


router = APIRouter(prefix="/api/v1")


router.include_router(endpoints.router)
