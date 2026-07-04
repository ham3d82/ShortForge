"""
AI Provider Factory.

Creates and returns the configured AI provider.
"""

from collections.abc import Callable

from app.core.config import settings
from app.providers.base import AIProvider
from app.providers.gemini_provider.provider import GeminiProvider


PROVIDERS: dict[str, Callable[[], AIProvider]] = {
    "gemini": GeminiProvider,
}


def get_provider() -> AIProvider:
    """Return the configured AI provider."""

    provider_factory = PROVIDERS.get(settings.AI_PROVIDER)

    if provider_factory is None:
        supported = ", ".join(PROVIDERS.keys())

        raise ValueError(
            f"Unsupported AI provider: {settings.AI_PROVIDER}. "
            f"Supported providers: {supported}"
        )

    return provider_factory()