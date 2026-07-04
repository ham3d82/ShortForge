"""
Gemini text generation implementation.
"""

from typing import Type

from google import genai
from pydantic import BaseModel

from app.providers.gemini_provider.utils import execute_with_retry


class GeminiTextGenerator:
    """Handles all Gemini text generation operations."""

    def __init__(
        self,
        client: genai.Client,
        model: str,
    ) -> None:
        self.client = client
        self.model = model

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate plain text.
        """

        response = await execute_with_retry(
            self.client.models.generate_content,
            model=self.model,
            contents=prompt,
        )

        return response.text or ""

    async def generate_structured(
        self,
        prompt: str,
        schema: Type[BaseModel],
    ) -> BaseModel:
        """
        Generate structured JSON validated by Pydantic.
        """

        response = await execute_with_retry(
            self.client.models.generate_content,
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        return response.parsed