"""
Base video provider interface.

All video providers (MoviePy, FFmpeg, etc.)
must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseVideoProvider(ABC):
    """Abstract base class for video providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        raise NotImplementedError

    @abstractmethod
    async def generate(
        self,
        image_paths: list[str],
        audio_path: str,
        output_path: Path,
        **kwargs: Any,
    ) -> Path:
        """
        Generate a video.

        Args:
            image_paths:
                Local image paths.

            audio_path:
                Local audio file path.

            output_path:
                Absolute output path.

        Returns:
            Absolute path to the generated video.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(
        self,
    ) -> bool:
        """Verify the provider is available."""
        raise NotImplementedError