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
    """
    Centralized application settings.

    All configuration values should be defined here and loaded
    from environment variables or the .env file.
    """

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME: str = "ShortForge"

    APP_VERSION: str = "0.1.0"

    DEBUG: bool = True

    ENVIRONMENT: str = "development"

    # ==========================================================
    # Server
    # ==========================================================

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    # ==========================================================
    # API
    # ==========================================================

    API_V1_PREFIX: str = "/api/v1"

    # ==========================================================
    # CORS
    # ==========================================================

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # ==========================================================
    # Logging
    # ==========================================================

    LOG_LEVEL: str = "DEBUG"

    LOG_FORMAT: str = "console"

    # ==========================================================
    # AI Providers
    # ==========================================================

    AI_PROVIDER: str = "gemini"

    IMAGE_PROVIDER: str = "pollinations"

    SPEECH_PROVIDER: str = "gtts"

    AI_TIMEOUT: int = 60

    # ==========================================================
    # Gemini
    # ==========================================================

    GEMINI_API_KEY: str = ""

    GEMINI_TEXT_MODEL: str = "gemini-2.5-flash"

    GEMINI_IMAGE_MODEL: str = "imagen-4.0-generate-001"

    # ==========================================================
    # Pollinations
    # ==========================================================

    POLLINATIONS_BASE_URL: str = (
        "https://image.pollinations.ai/prompt"
    )

    # ==========================================================
    # OpenAI
    # ==========================================================

    OPENAI_API_KEY: str = ""

    OPENAI_TEXT_MODEL: str = "gpt-5"

    OPENAI_IMAGE_MODEL: str = "gpt-image-1"

    # ==========================================================
    # OpenRouter
    # ==========================================================

    OPENROUTER_API_KEY: str = ""

    OPENROUTER_BASE_URL: str = (
        "https://openrouter.ai/api/v1"
    )

    OPENROUTER_TEXT_MODEL: str = ""

    # ==========================================================
    # Speech
    # ==========================================================

    GTTS_DEFAULT_LANGUAGE: str = "en"

    # ==========================================================
    # Database
    # ==========================================================

    DATABASE_URL: str

    DATABASE_SYNC_URL: str

    REDIS_URL: str

    # ==========================================================
    # Paths
    # ==========================================================

    PROJECT_ROOT: Path = (
        Path(__file__)
        .resolve()
        .parent.parent.parent.parent
    )

    GENERATED_IMAGES_DIR: Path = (
        PROJECT_ROOT / "generated_images"
    )

    GENERATED_AUDIO_DIR: Path = (
        PROJECT_ROOT / "generated_audio"
    )

    # ==========================================================
    # Validators
    # ==========================================================

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(
        cls,
        value: str,
    ) -> str:
        allowed = {
            "development",
            "testing",
            "production",
        }

        if value.lower() not in allowed:
            raise ValueError(
                f"ENVIRONMENT must be one of {allowed}"
            )

        return value.lower()

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(
        cls,
        value: str,
    ) -> str:
        allowed = {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }

        if value.upper() not in allowed:
            raise ValueError(
                f"LOG_LEVEL must be one of {allowed}"
            )

        return value.upper()

    @field_validator("PORT")
    @classmethod
    def validate_port(
        cls,
        value: int,
    ) -> int:
        if not (1 <= value <= 65535):
            raise ValueError(
                "PORT must be between 1 and 65535"
            )

        return value
    @field_validator("AI_PROVIDER")
    @classmethod
    def validate_ai_provider(
        cls,
        value: str,
    ) -> str:
        allowed = {
            "gemini",
            "openai",
            "openrouter",
        }

        if value.lower() not in allowed:
            raise ValueError(
                f"AI_PROVIDER must be one of {allowed}"
            )

        return value.lower()

    @field_validator("IMAGE_PROVIDER")
    @classmethod
    def validate_image_provider(
        cls,
        value: str,
    ) -> str:
        allowed = {
            "pollinations",
            "gemini",
        }

        if value.lower() not in allowed:
            raise ValueError(
                f"IMAGE_PROVIDER must be one of {allowed}"
            )

        return value.lower()

    @field_validator("SPEECH_PROVIDER")
    @classmethod
    def validate_speech_provider(
        cls,
        value: str,
    ) -> str:
        allowed = {
            "gtts",
        }

        if value.lower() not in allowed:
            raise ValueError(
                f"SPEECH_PROVIDER must be one of {allowed}"
            )

        return value.lower()

    @field_validator("AI_TIMEOUT")
    @classmethod
    def validate_ai_timeout(
        cls,
        value: int,
    ) -> int:
        if value <= 0:
            raise ValueError(
                "AI_TIMEOUT must be greater than 0"
            )

        return value

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