"""
CrediLens — Health Endpoint
"""

from fastapi import APIRouter
from backend.app.schemas.common import ApiResponse
from backend.app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=ApiResponse[dict])
async def health_check():
    return ApiResponse(
        success=True,
        data={
            "status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION
        },
        error=None
    )
