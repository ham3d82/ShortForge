"""
AI dependencies.
"""

from app.providers.text.factory import get_text_provider
from app.services.ai_service import AIService


def get_ai_service() -> AIService:
    """Return an AI service instance."""

    return AIService(
        text_provider=get_text_provider(),
    )