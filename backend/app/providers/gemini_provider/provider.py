"""
Google Gemini text provider implementation.
"""

from google import genai
from pydantic import BaseModel

from app.core.config import settings
from app.providers.gemini_provider.text import GeminiTextGenerator
from app.providers.text.base import TextProvider


class GeminiProvider(TextProvider):
    """Google Gemini text provider."""

    @property
    def provider_name(self) -> str:
        return "gemini"

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.text = GeminiTextGenerator(
            client=self.client,
            model=settings.GEMINI_TEXT_MODEL,
        )

    async def generate(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        """
        Generate plain text.
        """

        return await self.text.generate(
            prompt=prompt,
        )

    async def generate_structured(
        self,
        prompt: str,
        schema: type[BaseModel],
        **kwargs,
    ) -> BaseModel:
        """
        Generate structured output.
        """

        return await self.text.generate_structured(
            prompt=prompt,
            schema=schema,
        )

    async def health_check(
        self,
    ) -> bool:
        """
        Check provider configuration.
        """

        return bool(settings.GEMINI_API_KEY)