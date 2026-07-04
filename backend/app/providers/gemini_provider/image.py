"""
Gemini image generation implementation.
"""

from google import genai


class GeminiImageGenerator:
    """Handles Gemini image generation."""

    def __init__(
        self,
        client: genai.Client,
        model: str,
    ) -> None:
        self.client = client
        self.model = model

    async def generate_image(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an image from a prompt.

        NOTE:
        This method will be implemented after the provider
        refactor is completed.
        """

        raise NotImplementedError(
            "Image generation is not implemented yet."
        )