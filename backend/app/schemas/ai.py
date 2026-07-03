"""
AI request/response schemas.
"""

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """Request body for AI text generation."""

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Prompt sent to the AI model.",
    )


class GenerateResponse(BaseModel):
    """Response returned from AI generation."""

    text: str = Field(
        ...,
        description="Generated text.",
    )