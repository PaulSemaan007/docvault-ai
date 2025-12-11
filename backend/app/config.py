"""
Application configuration using Pydantic Settings.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "DocVault AI"
    debug: bool = False

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""

    # JWT
    jwt_secret: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24  # 24 hours

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://docvault-ai.vercel.app",
    ]

    # File Upload
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: List[str] = [".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx", ".txt"]

    # ML Models
    classifier_model: str = "distilbert-base-uncased"
    spacy_model: str = "en_core_web_sm"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
