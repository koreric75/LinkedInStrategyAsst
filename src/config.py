"""
Configuration module for LinkedIn Strategy Assistant.

Centralizes all configuration values with environment variable support.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List


class Config:
    """Application configuration with environment variable support."""
    
    # Application Settings
    APP_TITLE: str = "LinkedIn Strategy Assistant"
    APP_VERSION: str = "1.2.0"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS", 
        "*"
    ).split(",")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", str(10 * 1024 * 1024)))  # 10MB default
    ALLOWED_RESUME_EXTENSIONS: List[str] = [".pdf", ".docx", ".doc", ".txt"]
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".png", ".jpg", ".jpeg"]
    
    # OCR Settings
    USE_CLOUD_VISION_DEFAULT: bool = os.getenv("USE_CLOUD_VISION_DEFAULT", "true").lower() == "true"
    TESSERACT_CMD: str = os.getenv("TESSERACT_CMD", "tesseract")
    
    # Firebase Settings
    FIREBASE_ADMIN_SDK_PATH: Path = Path(os.getenv("FIREBASE_ADMIN_SDK_PATH", "firebase-adminsdk.json"))
    FIREBASE_ENABLED: bool = False  # Set dynamically during initialization
    
    # Google Cloud Settings
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "linkedin-strategy-ai-assistant")
    GCP_REGION: str = os.getenv("GCP_REGION", "us-central1")
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Strategy Generation Settings
    PROFILE_SCORE_MIN: int = 0
    PROFILE_SCORE_MAX: int = 100
    PROFILE_SCORE_BASELINE: int = 70
    
    # Advanced Tech Terms for Gap Analysis
    ADVANCED_TECH_TERMS: List[str] = [
        "LLM", "RPA", "Docker", "Kubernetes", "Cloud Run", "CI/CD",
        "Terraform", "AI", "Machine Learning", "Cloud-native",
        "FastAPI", "Flutter", "Microservices", "Serverless",
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration values."""
        if cls.PORT < 1 or cls.PORT > 65535:
            raise ValueError(f"Invalid PORT: {cls.PORT}")
        if cls.MAX_UPLOAD_SIZE < 1:
            raise ValueError(f"Invalid MAX_UPLOAD_SIZE: {cls.MAX_UPLOAD_SIZE}")
        return True


# Initialize and validate config on import
Config.validate()
