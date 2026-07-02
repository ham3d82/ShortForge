"""
AI Provider Factory.

Creates and returns the configured AI provider.
"""

from app.core.config import settings
from app.providers.base import AIProvider
from app.providers.gemini import GeminiProvider


def get_provider() -> AIProvider:
    """Return the configured AI provider."""

    if settings.AI_PROVIDER == "gemini":
        return GeminiProvider()

    raise ValueError(f"Unsupported AI provider: {settings.AI_PROVIDER}")