"""
Base image provider interface.

All image providers (Gemini, OpenAI, etc.)
must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ImageProvider(ABC):
    """Abstract base class for image providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        raise NotImplementedError

    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a single image.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify the provider is available."""
        raise NotImplementedError