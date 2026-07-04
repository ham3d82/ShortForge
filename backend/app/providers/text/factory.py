"""
Text provider factory.

Creates and returns the configured text provider.
"""

from collections.abc import Callable

from app.core.config import settings
from app.providers.text.base import TextProvider
from app.providers.text.gemini import GeminiTextProvider


TEXT_PROVIDERS: dict[str, Callable[[], TextProvider]] = {
    "gemini": GeminiTextProvider,
}


def get_text_provider() -> TextProvider:
    """Return the configured text provider."""

    provider_factory = TEXT_PROVIDERS.get(settings.AI_PROVIDER)

    if provider_factory is None:
        supported = ", ".join(TEXT_PROVIDERS.keys())

        raise ValueError(
            f"Unsupported text provider: {settings.AI_PROVIDER}. "
            f"Supported providers: {supported}"
        )

    return provider_factory()