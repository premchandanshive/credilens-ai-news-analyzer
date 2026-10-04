"""
CrediLens — Analysis Management & History Routes
"""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.analysis import AnalysisResponse, HistoryListResponse
from backend.app.database.repositories import analysis_repo
from backend.app.services.report_service import report_service
from backend.app.api.deps import get_optional_user
from backend.app.core.errors import NotFoundException

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/history", response_model=ApiResponse[HistoryListResponse])
async def get_analysis_history(
    q: Optional[str] = Query(None),
    sort: str = Query("createdAt_desc"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: Optional[dict] = Depends(get_optional_user)
):
    user_id = current_user["id"] if current_user else None
    history_data = await analysis_repo.list_analyses(
        user_id=user_id,
        query=q,
        sort=sort,
        page=page,
        limit=limit
    )
    return ApiResponse(success=True, data=history_data, error=None)

@router.get("/{analysis_id}", response_model=ApiResponse[AnalysisResponse])
async def get_analysis_detail(analysis_id: str):
    analysis = await analysis_repo.get_by_id(analysis_id)
    if not analysis:
        raise NotFoundException(f"Analysis '{analysis_id}' not found.")
    return ApiResponse(success=True, data=analysis, error=None)

@router.delete("/{analysis_id}", response_model=ApiResponse[dict])
async def delete_analysis(analysis_id: str):
    deleted = await analysis_repo.delete(analysis_id)
    if not deleted:
        raise NotFoundException(f"Analysis '{analysis_id}' not found.")
    return ApiResponse(success=True, data={"deleted": True, "id": analysis_id}, error=None)

@router.get("/{analysis_id}/report", response_model=ApiResponse[dict])
async def get_analysis_report(analysis_id: str):
    report_data = await report_service.generate_report_payload(analysis_id)
    return ApiResponse(success=True, data=report_data, error=None)
