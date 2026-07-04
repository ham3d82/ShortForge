"""
Application configuration using pydantic-settings.

Loads configuration from environment variables and .env file.
Provides typed access to all configuration values.
"""

import sys
from pathlib import Path

from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    APP_NAME: str = "ShortForge"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # ------------------------------------------------------------------
    # Server
    # ------------------------------------------------------------------

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    API_V1_PREFIX: str = "/api/v1"

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "console"

    # ------------------------------------------------------------------
    # AI
    # ------------------------------------------------------------------

    AI_PROVIDER: str = "gemini"

    IMAGE_PROVIDER: str = "pollinations"

    AI_TIMEOUT: int = 60

    # ------------------------------------------------------------------
    # Gemini
    # ------------------------------------------------------------------

    GEMINI_API_KEY: str = ""

    GEMINI_TEXT_MODEL: str = "gemini-2.5-flash"

    GEMINI_IMAGE_MODEL: str = "imagen-4.0-generate-001"

    # ------------------------------------------------------------------
    # Pollinations
    # ------------------------------------------------------------------

    POLLINATIONS_BASE_URL: str = "https://image.pollinations.ai/prompt"

    # ------------------------------------------------------------------
    # OpenAI
    # ------------------------------------------------------------------

    OPENAI_API_KEY: str = ""

    OPENAI_TEXT_MODEL: str = "gpt-5"

    OPENAI_IMAGE_MODEL: str = "gpt-image-1"

    # ------------------------------------------------------------------
    # OpenRouter
    # ------------------------------------------------------------------

    OPENROUTER_API_KEY: str = ""

    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    OPENROUTER_TEXT_MODEL: str = ""

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    DATABASE_URL: str

    DATABASE_SYNC_URL: str

    REDIS_URL: str

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent

    GENERATED_IMAGES_DIR: Path = PROJECT_ROOT / "generated_images"

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

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

    @field_validator("AI_PROVIDER")
    @classmethod
    def validate_ai_provider(cls, v: str) -> str:
        allowed = {
            "gemini",
            "openai",
            "openrouter",
        }

        if v.lower() not in allowed:
            raise ValueError(f"AI_PROVIDER must be one of {allowed}")

        return v.lower()

    @field_validator("IMAGE_PROVIDER")
    @classmethod
    def validate_image_provider(cls, v: str) -> str:
        allowed = {
            "pollinations",
            "gemini",
        }

        if v.lower() not in allowed:
            raise ValueError(f"IMAGE_PROVIDER must be one of {allowed}")

        return v.lower()

    @field_validator("AI_TIMEOUT")
    @classmethod
    def validate_ai_timeout(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("AI_TIMEOUT must be greater than 0")

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
    print(
        f"Configuration validation failed:\n{exc}",
        file=sys.stderr,
    )

    sys.exit(1)