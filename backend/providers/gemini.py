"""
Google Gemini AI provider.
"""

from __future__ import annotations

from google import genai

from app.core.config import settings
from app.providers.base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini provider."""

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    @property
    def provider_name(self) -> str:
        return "gemini"

    async def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        raise NotImplementedError

    async def health_check(self) -> bool:
        raise NotImplementedError