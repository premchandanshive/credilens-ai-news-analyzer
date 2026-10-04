"""
CrediLens — Database Repositories
Implements dual-mode asynchronous persistence: MongoDB with in-memory fallback.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from backend.app.database.mongodb import db_manager

class BaseRepository:
    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

class UserRepository(BaseRepository):
    def __init__(self):
        self._mem_users: Dict[str, Dict[str, Any]] = {}
        # Seed default academic demo user
        from backend.app.core.security import hash_password
        demo_id = "user_demo_1"
        self._mem_users[demo_id] = {
            "_id": demo_id,
            "id": demo_id,
            "email": "demo@credilens.local",
            "passwordHash": hash_password("demo1234"),
            "displayName": "Prem Kumar",
            "role": "student",
            "preferences": {
                "theme": "dark",
                "maxClaims": 6,
                "includeTransformer": False
            },
            "createdAt": self._now_iso(),
            "updatedAt": self._now_iso()
        }

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        norm_email = email.strip().lower()
        if db_manager.is_connected and db_manager.db is not None:
            user = await db_manager.db.users.find_one({"email": norm_email})
            if user:
                user["id"] = str(user["_id"])
            return user
        
        for u in self._mem_users.values():
            if u["email"] == norm_email:
                return u
        return None

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            user = await db_manager.db.users.find_one({"_id": user_id})
            if user:
                user["id"] = str(user["_id"])
            return user
        return self._mem_users.get(user_id)

    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user_data["_id"] = user_id
        user_data["id"] = user_id
        user_data["createdAt"] = self._now_iso()
        user_data["updatedAt"] = self._now_iso()

        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db.users.insert_one(user_data)
        else:
            self._mem_users[user_id] = user_data
            
        return user_data

    async def update(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updates["updatedAt"] = self._now_iso()
        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db.users.update_one({"_id": user_id}, {"$set": updates})
            return await self.get_by_id(user_id)
        
        user = self._mem_users.get(user_id)
        if user:
            user.update(updates)
            return user
        return None

class AnalysisRepository(BaseRepository):
    def __init__(self):
        self._mem_analyses: Dict[str, Dict[str, Any]] = {}

    async def create(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        analysis_id = analysis_data.get("id") or f"ana_{uuid.uuid4().hex[:16]}"
        analysis_data["_id"] = analysis_id
        analysis_data["id"] = analysis_id
        if "createdAt" not in analysis_data:
            analysis_data["createdAt"] = self._now_iso()
        analysis_data["updatedAt"] = self._now_iso()

        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db.analyses.insert_one(analysis_data)
        else:
            self._mem_analyses[analysis_id] = analysis_data

        return analysis_data

    async def get_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            doc = await db_manager.db.analyses.find_one({"_id": analysis_id})
            if doc:
                doc["id"] = str(doc["_id"])
            return doc
        return self._mem_analyses.get(analysis_id)

    async def list_analyses(
        self,
        user_id: Optional[str] = None,
        query: Optional[str] = None,
        sort: str = "createdAt_desc",
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        items: List[Dict[str, Any]] = []

        if db_manager.is_connected and db_manager.db is not None:
            filter_q: Dict[str, Any] = {}
            if user_id:
                filter_q["userId"] = user_id
            if query:
                filter_q["$or"] = [
                    {"title": {"$regex": query, "$options": "i"}},
                    {"articleExcerpt": {"$regex": query, "$options": "i"}}
                ]

            cursor = db_manager.db.analyses.find(filter_q)
            sort_dir = -1 if "desc" in sort else 1
            cursor.sort("createdAt", sort_dir).skip((page - 1) * limit).limit(limit)

            total = await db_manager.db.analyses.count_documents(filter_q)
            async for doc in cursor:
                doc["id"] = str(doc["_id"])
                items.append(doc)
            return {"items": items, "total": total, "page": page, "limit": limit}

        # In-memory listing
        all_docs = list(self._mem_analyses.values())
        if user_id:
            all_docs = [d for d in all_docs if d.get("userId") == user_id]
        if query:
            q_lower = query.lower()
            all_docs = [
                d for d in all_docs
                if q_lower in (d.get("title") or "").lower() or q_lower in (d.get("articleExcerpt") or "").lower()
            ]

        # Sort
        reverse = "desc" in sort
        all_docs.sort(key=lambda d: d.get("createdAt", ""), reverse=reverse)

        total = len(all_docs)
        start = (page - 1) * limit
        end = start + limit
        paginated = all_docs[start:end]

        return {
            "items": paginated,
            "total": total,
            "page": page,
            "limit": limit
        }

    async def delete(self, analysis_id: str) -> bool:
        if db_manager.is_connected and db_manager.db is not None:
            res = await db_manager.db.analyses.delete_one({"_id": analysis_id})
            return res.deleted_count > 0
        if analysis_id in self._mem_analyses:
            del self._mem_analyses[analysis_id]
            return True
        return False

# Global repository instances
user_repo = UserRepository()
analysis_repo = AnalysisRepository()
