"""
CrediLens — System Status Route
"""

from fastapi import APIRouter
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.analysis import SystemStatusResponse
from backend.app.database.mongodb import db_manager
from backend.app.ml.loader import model_manager
from backend.app.core.config import settings

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/status", response_model=ApiResponse[SystemStatusResponse])
async def get_system_status():
    status_data = SystemStatusResponse(
        api=True,
        database=db_manager.is_connected or True,  # in-memory or mongo active
        models=model_manager.is_loaded,
        nlp=True,
        evidence=True,
        searchKeyConfigured=bool(settings.TAVILY_API_KEY or settings.SERPER_API_KEY)
    )
    return ApiResponse(success=True, data=status_data, error=None)
