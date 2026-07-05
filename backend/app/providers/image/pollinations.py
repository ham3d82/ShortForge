"""
Pollinations image provider implementation.
"""

from urllib.parse import quote

from app.core.config import settings
from app.providers.image.base import ImageProvider


class PollinationsImageProvider(ImageProvider):
    """Pollinations image provider."""

    @property
    def provider_name(self) -> str:
        return "pollinations"

    async def generate_image(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        """
        Generate an image URL from Pollinations.
        """

        encoded_prompt = quote(prompt)

        return (
            f"{settings.POLLINATIONS_BASE_URL}/"
            f"{encoded_prompt}"
        )

    async def health_check(
        self,
    ) -> bool:
        """
        Pollinations does not require an API key.
        """

        return True