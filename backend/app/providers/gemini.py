"""
Google Gemini AI provider implementation.
"""

import asyncio
from typing import Any, Type

from google import genai
from google.genai.errors import ServerError
from pydantic import BaseModel

from app.core.config import settings
from app.providers.base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini provider."""

    @property
    def provider_name(self) -> str:
        return "gemini"

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    async def health_check(self) -> bool:
        """Check whether the provider is configured."""
        return bool(settings.GEMINI_API_KEY)

    async def _generate(
        self,
        **kwargs: Any,
    ):
        """Execute a Gemini request with automatic retries."""

        last_error = None

        for attempt in range(3):
            try:
                return self.client.models.generate_content(**kwargs)

            except ServerError as exc:
                last_error = exc

                if attempt == 2:
                    raise

                await asyncio.sleep(2)

        raise last_error

    async def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Generate plain text."""

        response = await self._generate(
            model=self.model,
            contents=prompt,
        )

        return response.text or ""

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
        **kwargs: Any,
    ) -> BaseModel:
        """Generate structured output."""

        response = await self._generate(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        return response.parsed