"""
CrediLens — Application Configuration
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "CrediLens"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server & CORS
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FRONTEND_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"

    # Database
    MONGODB_URI: Optional[str] = None
    MONGODB_DB: str = "credilens"

    # Security & JWT
    JWT_SECRET: str = "credilens-academic-ai-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7

    # External Search Providers (optional keys with fallbacks)
    TAVILY_API_KEY: Optional[str] = None
    SERPER_API_KEY: Optional[str] = None

    # Analysis Defaults
    MAX_CLAIMS: int = 6
    ENABLE_TRANSFORMER: bool = False

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.FRONTEND_ORIGINS.split(",") if origin.strip()]

settings = Settings()
