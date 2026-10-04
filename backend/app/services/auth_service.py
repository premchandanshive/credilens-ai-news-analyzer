"""
CrediLens — Authentication Service
"""

from typing import Dict, Any, Optional
from backend.app.database.repositories import user_repo
from backend.app.core.security import hash_password, verify_password, create_access_token
from backend.app.core.errors import InvalidInputException, UnauthorizedException, NotFoundException

class AuthService:
    async def register(self, email: str, password: str, display_name: str) -> Dict[str, Any]:
        norm_email = email.strip().lower()
        existing = await user_repo.get_by_email(norm_email)
        if existing:
            raise InvalidInputException("An account with this email address already exists.")

        password_hash = hash_password(password)
        new_user = await user_repo.create({
            "email": norm_email,
            "passwordHash": password_hash,
            "displayName": display_name.strip(),
            "role": "student",
            "preferences": {
                "theme": "dark",
                "maxClaims": 6,
                "includeTransformer": False
            }
        })

        token = create_access_token(new_user["id"], new_user["email"])
        return {
            "token": token,
            "user": {
                "id": new_user["id"],
                "email": new_user["email"],
                "displayName": new_user["displayName"],
                "role": new_user.get("role", "student"),
                "preferences": new_user.get("preferences", {"theme": "dark", "maxClaims": 6, "includeTransformer": False})
            }
        }

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        norm_email = email.strip().lower()
        user = await user_repo.get_by_email(norm_email)
        if not user or not verify_password(password, user.get("passwordHash", "")):
            raise UnauthorizedException("Invalid email or password.")

        token = create_access_token(user["id"], user["email"])
        return {
            "token": token,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "displayName": user["displayName"],
                "role": user.get("role", "student"),
                "preferences": user.get("preferences", {"theme": "dark", "maxClaims": 6, "includeTransformer": False})
            }
        }

    async def get_profile(self, user_id: str) -> Dict[str, Any]:
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("User profile not found.")
        return {
            "id": user["id"],
            "email": user["email"],
            "displayName": user["displayName"],
            "role": user.get("role", "student"),
            "preferences": user.get("preferences", {"theme": "dark", "maxClaims": 6, "includeTransformer": False})
        }

    async def update_profile(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        cleaned_updates = {}
        if "displayName" in updates and updates["displayName"]:
            cleaned_updates["displayName"] = updates["displayName"].strip()
        if "preferences" in updates and updates["preferences"] is not None:
            cleaned_updates["preferences"] = updates["preferences"]

        user = await user_repo.update(user_id, cleaned_updates)
        if not user:
            raise NotFoundException("User not found.")
        return {
            "id": user["id"],
            "email": user["email"],
            "displayName": user["displayName"],
            "role": user.get("role", "student"),
            "preferences": user.get("preferences", {"theme": "dark", "maxClaims": 6, "includeTransformer": False})
        }

auth_service = AuthService()
