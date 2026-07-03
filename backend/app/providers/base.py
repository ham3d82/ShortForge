"""
Base AI provider interface.

All AI providers (Gemini, OpenAI, etc.) must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel


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
        """Generate plain text."""
        raise NotImplementedError

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
        **kwargs: Any,
    ) -> BaseModel:
        """
        Generate structured data validated against a Pydantic schema.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify the provider is available."""
        raise NotImplementedError