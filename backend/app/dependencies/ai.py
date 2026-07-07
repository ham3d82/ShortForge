"""
AI dependencies.
"""

from app.providers.image.factory import get_image_provider
from app.providers.speech.factory import get_speech_provider
from app.providers.text.factory import get_text_provider

from app.services.ai_service import AIService


def get_ai_service() -> AIService:
    """Return an AI service instance."""

    return AIService(
        text_provider=get_text_provider(),
        image_provider=get_image_provider(),
        speech_provider=get_speech_provider(),
    )