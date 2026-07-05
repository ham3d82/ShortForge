"""
Image provider factory.

Creates and returns the configured image provider.
"""

from collections.abc import Callable

from app.core.config import settings
from app.providers.image.base import ImageProvider
from app.providers.image.gemini import GeminiImageProvider
from app.providers.image.pollinations import PollinationsImageProvider


IMAGE_PROVIDERS: dict[str, Callable[[], ImageProvider]] = {
    "gemini": GeminiImageProvider,
    "pollinations": PollinationsImageProvider,
}


def get_image_provider() -> ImageProvider:
    """Return the configured image provider."""

    provider_factory = IMAGE_PROVIDERS.get(settings.IMAGE_PROVIDER)

    if provider_factory is None:
        supported = ", ".join(IMAGE_PROVIDERS.keys())

        raise ValueError(
            f"Unsupported image provider: {settings.IMAGE_PROVIDER}. "
            f"Supported providers: {supported}"
        )

    return provider_factory()