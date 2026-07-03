"""
Google Gemini AI provider implementation.
"""

from typing import Any

from google import genai

from app.core.config import settings

from app.providers.base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini provider."""

    @property
    def provider_name(self) -> str:
        return "gemini"

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    async def health_check(self) -> bool:
        """Check whether the provider is configured."""
        return bool(settings.GEMINI_API_KEY)

    async def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Generate text using Gemini."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text or ""