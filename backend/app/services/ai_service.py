"""
AI service.

Provides a single interface for the rest of the application
to communicate with the configured AI provider.
"""

from typing import Type

from pydantic import BaseModel

from app.providers.base import AIProvider


class AIService:
    """High-level AI service."""

    def __init__(
        self,
        provider: AIProvider,
    ) -> None:
        self.provider = provider

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate plain text."""
        return await self.provider.generate(prompt)

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        """Generate structured output."""
        return await self.provider.generate_structured(
            prompt=prompt,
            schema=schema,
        )

    async def health_check(self) -> bool:
        """Check provider health."""
        return await self.provider.health_check()