from fastapi import APIRouter

from src.router import v1

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(v1.file.router)
router.include_router(v1.user.router)
