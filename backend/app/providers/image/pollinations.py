"""
Pollinations image provider implementation.
"""

from urllib.parse import quote

import httpx

from app.core.config import settings
from app.providers.image.base import ImageProvider
from app.services.image_storage import ImageStorageService


class PollinationsImageProvider(ImageProvider):
    """Pollinations image provider."""

    @property
    def provider_name(self) -> str:
        return "pollinations"

    def __init__(self) -> None:
        self.storage = ImageStorageService()

    async def generate_image(
        self,
        prompt: str,
        **kwargs,
    ) -> str:
        """
        Generate an image and save it locally.
        """

        encoded_prompt = quote(prompt)

        image_url = (
            f"{settings.POLLINATIONS_BASE_URL}/"
            f"{encoded_prompt}"
        )

        async with httpx.AsyncClient(timeout=settings.AI_TIMEOUT) as client:
            response = await client.get(image_url)

            response.raise_for_status()

        image_path = await self.storage.save_image(
            image_bytes=response.content,
            extension="png",
        )

        return image_path

    async def health_check(self) -> bool:
        """
        Pollinations does not require an API key.
        """

        return True