"""
Base AI provider interface.

All AI providers (Gemini, OpenAI, etc.) must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
        raise NotImplementedError

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a text response from the given prompt.

        Args:
            prompt: User prompt.
            **kwargs: Provider-specific options.

        Returns:
            Generated text.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify the provider is available.

        Returns:
            True if healthy.
        """
        raise NotImplementedError