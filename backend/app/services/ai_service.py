"""
AI service.

Provides a single interface for the rest of the application
to communicate with the configured AI provider.
"""

from app.providers.factory import get_provider


class AIService:
    """High-level AI service."""

    def __init__(self) -> None:
        self.provider = get_provider()

    async def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate text using the configured provider."""
        return await self.provider.generate(prompt)

    async def health_check(self) -> bool:
        """Check provider health."""
        return await self.provider.health_check()