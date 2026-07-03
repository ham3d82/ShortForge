"""
AI dependencies.
"""

from app.services.ai_service import AIService


def get_ai_service() -> AIService:
    """Return an AI service instance."""
    return AIService()