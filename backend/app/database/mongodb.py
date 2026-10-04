"""
CrediLens — MongoDB Connection Manager & Fallback
Provides async Motor client integration with resilient in-memory storage fallback.
"""

from typing import Optional, Any
from backend.app.core.config import settings

class DatabaseManager:
    _instance: Optional['DatabaseManager'] = None

    def __init__(self):
        self.client: Optional[Any] = None
        self.db: Optional[Any] = None
        self._is_connected: bool = False

    @classmethod
    def get_instance(cls) -> 'DatabaseManager':
        if cls._instance is None:
            cls._instance = DatabaseManager()
        return cls._instance

    async def connect(self):
        """Establish async connection to MongoDB if URI is configured."""
        if not settings.MONGODB_URI:
            print("[Database] No MONGODB_URI configured. Running in in-memory repository mode.")
            self._is_connected = False
            return

        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=4000
            )
            self.db = self.client[settings.MONGODB_DB]
            # Ping database to verify connection
            await self.client.admin.command('ping')
            self._is_connected = True
            print(f"[Database] Connected successfully to MongoDB: {settings.MONGODB_DB}")
            
            # Setup indexes asynchronously
            await self._setup_indexes()
        except Exception as e:
            print(f"[Database] Could not connect to MongoDB ({e}). Falling back to in-memory mode.")
            self.client = None
            self.db = None
            self._is_connected = False

    async def _setup_indexes(self):
        if self.db is None:
            return
        try:
            # Users unique email index
            await self.db.users.create_index("email", unique=True)
            # Analyses indexes
            await self.db.analyses.create_index("createdAt")
            await self.db.analyses.create_index("userId")
        except Exception as e:
            print(f"[Database] Index creation notice: {e}")

    async def disconnect(self):
        if self.client is not None:
            self.client.close()
            self._is_connected = False
            print("[Database] MongoDB connection closed.")

    @property
    def is_connected(self) -> bool:
        return self._is_connected

db_manager = DatabaseManager.get_instance()
