"""
AI service.

Provides a single interface for the rest of the application
to communicate with the configured AI providers.
"""

from typing import Type

from pydantic import BaseModel

from app.providers.image.base import ImageProvider
from app.providers.speech.base import BaseSpeechProvider
from app.providers.text.base import TextProvider


class AIService:
    """High-level AI service."""

    def __init__(
        self,
        text_provider: TextProvider,
        image_provider: ImageProvider,
        speech_provider: BaseSpeechProvider,
    ) -> None:
        self.text_provider = text_provider
        self.image_provider = image_provider
        self.speech_provider = speech_provider

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

    async def generate_image(
        self,
        prompt: str,
    ) -> str:
        """Generate a single image."""

        return await self.image_provider.generate_image(
            prompt=prompt,
        )

    async def generate_speech(
        self,
        text: str,
        language: str,
    ) -> bytes:
        """Generate speech audio."""

        return await self.speech_provider.generate(
            text=text,
            language=language,
        )

    async def health_check(self) -> bool:
        """Check text provider health."""

        return await self.text_provider.health_check()