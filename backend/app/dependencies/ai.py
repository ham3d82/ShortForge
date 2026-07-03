"""
AI dependencies.
"""

from app.providers.factory import get_provider
from app.services.ai_service import AIService


def get_ai_service() -> AIService:
    """Return an AI service instance."""

    provider = get_provider()

    return AIService(provider)