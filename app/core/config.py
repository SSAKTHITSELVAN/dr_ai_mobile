
# =======================
# File: app/core/config.py
# Path: app/core/config.py
# =======================

from pydantic.v1 import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App settings
    app_name: str = "AI Health Companion"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./health_companion.db"
    
    # AI Settings
    gemini_api_key: str = "AIzaSyDEzVsTrDG0UnCGusugZjzNKkzSKgKyUJc"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    access_token_expire_minutes: int = 30
    
    # File upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"

settings = Settings()