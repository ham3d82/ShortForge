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
    ):
        """
        Generate an image from a prompt.

        Returns:
            The raw Gemini response. Saving the image is handled
            by the image service.
        """

        response = self.client.models.generate_images(
            model=self.model,
            prompt=prompt,
        )

        return response