"""
CrediLens — Sources Route
"""

from fastapi import APIRouter
from backend.app.schemas.common import ApiResponse
from backend.app.database.repositories import analysis_repo
from backend.app.core.errors import NotFoundException

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.get("/{source_id}", response_model=ApiResponse[dict])
async def get_source_detail(source_id: str):
    # Find source by searching stored analyses
    history = await analysis_repo.list_analyses(limit=50)
    for analysis in history.get("items", []):
        for s in analysis.get("sources", []):
            if s.get("id") == source_id or s.get("url") == source_id:
                return ApiResponse(success=True, data=s, error=None)
                
    raise NotFoundException(f"Source with id or URL '{source_id}' not found.")
