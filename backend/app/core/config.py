"""
Application configuration using pydantic-settings.

Loads configuration from environment variables and .env file.
Provides typed access to all configuration values.
"""

import sys
from pathlib import Path

from pydantic import field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "ShortForge"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # Logging
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "console"

    # API
    API_V1_PREFIX: str = "/api/v1"

    # Paths
    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "testing", "production"}
        if v.lower() not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v.lower()

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()

    @field_validator("PORT")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not (1 <= v <= 65535):
            raise ValueError("PORT must be between 1 and 65535")
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


try:
    settings = Settings()
except ValidationError as exc:
    print(f"Configuration validation failed:\n{exc}", file=sys.stderr)
    sys.exit(1)
