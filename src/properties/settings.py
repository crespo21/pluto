"""Application settings and configuration management."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_TITLE: str = os.getenv("API_TITLE", "Pluto API")
    API_DESCRIPTION: str = os.getenv("API_DESCRIPTION", "Clean architecture example API for user management")
    API_VERSION: str = os.getenv("API_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "0").lower() in ("1", "true", "yes")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "0").lower() in ("1", "true", "yes")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pluto.db")
    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "0").lower() in ("1", "true", "yes")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


# Global settings instance
settings = Settings()