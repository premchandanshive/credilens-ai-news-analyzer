"""
CrediLens — API Dependencies & Authentication
"""

from typing import Optional, Dict, Any
from fastapi import Header
from backend.app.core.security import decode_access_token
from backend.app.database.repositories import user_repo
from backend.app.core.errors import UnauthorizedException

async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """Require valid JWT access token in Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException("Authorization header with Bearer token is required.")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise UnauthorizedException("Invalid or expired authentication token.")

    user = await user_repo.get_by_id(payload["sub"])
    if not user:
        raise UnauthorizedException("Authenticated user account was not found.")

    return user

async def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """Extract authenticated user if valid token present, or None for guest requests."""
    if not authorization or not authorization.startswith("Bearer "):
        return None

    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        if payload and "sub" in payload:
            return await user_repo.get_by_id(payload["sub"])
    except Exception:
        pass
    return None
