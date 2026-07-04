"""
Google Gemini AI provider implementation.
"""

from google import genai

from app.core.config import settings
from app.providers.base import AIProvider
from app.providers.gemini_provider.image import GeminiImageGenerator
from app.providers.gemini_provider.text import GeminiTextGenerator


class GeminiProvider(AIProvider):
    """Google Gemini provider."""

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

        self.image = GeminiImageGenerator(
            client=self.client,
            model=settings.GEMINI_IMAGE_MODEL,
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
        schema,
        **kwargs,
    ):
        """
        Generate structured output.
        """

        return await self.text.generate_structured(
            prompt=prompt,
            schema=schema,
        )

    async def generate_image(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        """
        Generate an image.
        """

        return await self.image.generate_image(
            prompt=prompt,
        )

    async def health_check(
        self,
    ) -> bool:
        """
        Check provider configuration.
        """

        return bool(settings.GEMINI_API_KEY)