"""
CrediLens — Analysis Input & SSE Progress Routes
"""

import json
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.analysis import (
    AnalyzeTextRequest,
    AnalyzeUrlRequest,
    AnalysisResponse
)
from backend.app.services.analysis_orchestrator import orchestrator
from backend.app.services.extraction import extract_from_url, extract_from_file
from backend.app.api.deps import get_optional_user

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.post("/text", response_model=ApiResponse[AnalysisResponse])
async def analyze_text(
    body: AnalyzeTextRequest,
    current_user: Optional[dict] = Depends(get_optional_user)
):
    user_id = current_user["id"] if current_user else None
    max_claims = current_user.get("preferences", {}).get("maxClaims", 6) if current_user else 6

    result = await orchestrator.run_analysis(
        input_type="text",
        text=body.text,
        title=body.title,
        user_id=user_id,
        max_claims=max_claims
    )
    return ApiResponse(success=True, data=result, error=None)

@router.post("/url", response_model=ApiResponse[AnalysisResponse])
async def analyze_url(
    body: AnalyzeUrlRequest,
    current_user: Optional[dict] = Depends(get_optional_user)
):
    user_id = current_user["id"] if current_user else None
    max_claims = current_user.get("preferences", {}).get("maxClaims", 6) if current_user else 6

    extracted = await extract_from_url(body.url)
    
    result = await orchestrator.run_analysis(
        input_type="url",
        text=extracted["text"],
        title=extracted["title"],
        input_url=body.url,
        user_id=user_id,
        max_claims=max_claims
    )
    return ApiResponse(success=True, data=result, error=None)

@router.post("/file", response_model=ApiResponse[AnalysisResponse])
async def analyze_file(
    file: UploadFile = File(...),
    current_user: Optional[dict] = Depends(get_optional_user)
):
    user_id = current_user["id"] if current_user else None
    max_claims = current_user.get("preferences", {}).get("maxClaims", 6) if current_user else 6

    content = await file.read()
    extracted = extract_from_file(file.filename or "uploaded_document.txt", content)

    result = await orchestrator.run_analysis(
        input_type="file",
        text=extracted["text"],
        title=extracted["title"],
        file_name=file.filename,
        user_id=user_id,
        max_claims=max_claims
    )
    return ApiResponse(success=True, data=result, error=None)

@router.get("/{analysis_id}/events")
async def stream_analysis_progress(analysis_id: str):
    """Server-Sent Events endpoint streaming realtime progress updates."""
    async def event_publisher():
        async for event in orchestrator.event_generator(analysis_id):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(
        event_publisher(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
