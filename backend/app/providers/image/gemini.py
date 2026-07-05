"""
Gemini image provider implementation.
"""

from google import genai

from app.core.config import settings
from app.providers.gemini_provider.image import GeminiImageGenerator
from app.providers.image.base import ImageProvider


class GeminiImageProvider(ImageProvider):
    """Google Gemini image provider."""

    @property
    def provider_name(self) -> str:
        return "gemini"

    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.image = GeminiImageGenerator(
            client=self.client,
            model=settings.GEMINI_IMAGE_MODEL,
        )

    async def generate_image(
        self,
        prompt: str,
        **kwargs,
    ):
        """
        Generate an image.
        """

        return await self.image.generate_image(
            prompt=prompt,
        )

    async def health_check(self) -> bool:
        """
        Check provider configuration.
        """

        return bool(settings.GEMINI_API_KEY)