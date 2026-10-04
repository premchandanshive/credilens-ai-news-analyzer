"""
CrediLens — Authentication & User Schemas
"""

from typing import Optional, Literal
from pydantic import BaseModel, Field

class UserPreferences(BaseModel):
    theme: Literal["dark", "light"] = "dark"
    maxClaims: int = Field(default=6, ge=1, le=20)
    includeTransformer: bool = False

class RegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=6, max_length=128)
    displayName: str = Field(min_length=2, max_length=64)

class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str

class UserProfile(BaseModel):
    id: str
    email: str
    displayName: str
    role: str = "student"
    preferences: UserPreferences

class AuthTokenResponse(BaseModel):
    token: str
    user: UserProfile

class UpdateProfileRequest(BaseModel):
    displayName: Optional[str] = None
    preferences: Optional[UserPreferences] = None
