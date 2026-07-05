"""
AI request/response schemas.
"""

from pydantic import BaseModel, Field


# ------------------------------------------------------------------
# Text Generation
# ------------------------------------------------------------------


class GenerateRequest(BaseModel):
    """Request body for AI text generation."""

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Prompt sent to the AI model.",
    )


class GenerateResponse(BaseModel):
    """Response returned from AI text generation."""

    text: str = Field(
        ...,
        description="Generated text.",
    )


# ------------------------------------------------------------------
# Image Generation
# ------------------------------------------------------------------


class GenerateImageRequest(BaseModel):
    """Request body for AI image generation."""

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Prompt used to generate an image.",
    )


class GenerateImageResponse(BaseModel):
    """Response returned from AI image generation."""

    image_url: str = Field(
        ...,
        description="URL of the generated image.",
    )