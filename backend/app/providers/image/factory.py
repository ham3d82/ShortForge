"""
Image provider factory.

Creates and returns the configured image provider.
"""

from collections.abc import Callable

from app.core.config import settings
from app.providers.gemini_provider.provider import GeminiProvider
from app.providers.image.base import ImageProvider


IMAGE_PROVIDERS: dict[str, Callable[[], ImageProvider]] = {
    "gemini": GeminiProvider,
}


def get_image_provider() -> ImageProvider:
    """Return the configured image provider."""

    provider_factory = IMAGE_PROVIDERS.get(settings.AI_PROVIDER)

    if provider_factory is None:
        supported = ", ".join(IMAGE_PROVIDERS.keys())

        raise ValueError(
            f"Unsupported image provider: {settings.AI_PROVIDER}. "
            f"Supported providers: {supported}"
        )

    return provider_factory()