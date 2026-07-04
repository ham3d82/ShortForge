"""
AI service.

Provides a single interface for the rest of the application
to communicate with the configured text provider.
"""

from typing import Type

from pydantic import BaseModel

from app.providers.text.base import TextProvider


class AIService:
    """High-level AI service."""

    def __init__(
        self,
        text_provider: TextProvider,
    ) -> None:
        self.text_provider = text_provider

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate plain text."""

        return await self.text_provider.generate(
            prompt=prompt,
        )

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        """Generate structured output."""

        return await self.text_provider.generate_structured(
            prompt=prompt,
            schema=schema,
        )

    async def health_check(self) -> bool:
        """Check provider health."""

        return await self.text_provider.health_check()