"""
CrediLens — Authentication Routes
"""

from fastapi import APIRouter, Depends
from backend.app.schemas.common import ApiResponse
from backend.app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthTokenResponse,
    UserProfile,
    UpdateProfileRequest
)
from backend.app.services.auth_service import auth_service
from backend.app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=ApiResponse[AuthTokenResponse])
async def register_user(body: RegisterRequest):
    result = await auth_service.register(
        email=body.email,
        password=body.password,
        display_name=body.displayName
    )
    return ApiResponse(success=True, data=result, error=None)

@router.post("/login", response_model=ApiResponse[AuthTokenResponse])
async def login_user(body: LoginRequest):
    result = await auth_service.login(
        email=body.email,
        password=body.password
    )
    return ApiResponse(success=True, data=result, error=None)

@router.post("/logout", response_model=ApiResponse[None])
async def logout_user(current_user: dict = Depends(get_current_user)):
    return ApiResponse(success=True, data=None, error=None)

@router.get("/me", response_model=ApiResponse[UserProfile])
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    profile = await auth_service.get_profile(current_user["id"])
    return ApiResponse(success=True, data=profile, error=None)

@router.patch("/me", response_model=ApiResponse[UserProfile])
async def update_current_user_profile(
    body: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    updates = body.model_dump(exclude_none=True)
    profile = await auth_service.update_profile(current_user["id"], updates)
    return ApiResponse(success=True, data=profile, error=None)
