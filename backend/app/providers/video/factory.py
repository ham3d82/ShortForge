"""
Video provider factory.

Creates and returns the configured video provider.
"""

from collections.abc import Callable

from app.core.config import settings
from app.providers.video.base import BaseVideoProvider
from app.providers.video.moviepy import MoviePyVideoProvider


VIDEO_PROVIDERS: dict[
    str,
    Callable[[], BaseVideoProvider],
] = {
    "moviepy": MoviePyVideoProvider,
}


def get_video_provider() -> BaseVideoProvider:
    """Return the configured video provider."""

    provider_factory = VIDEO_PROVIDERS.get(
        settings.VIDEO_PROVIDER,
    )

    if provider_factory is None:
        supported = ", ".join(
            VIDEO_PROVIDERS.keys(),
        )

        raise ValueError(
            f"Unsupported video provider: "
            f"{settings.VIDEO_PROVIDER}. "
            f"Supported providers: {supported}"
        )

    return provider_factory()