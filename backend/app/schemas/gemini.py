"""
Schemas used for structured Gemini responses.
"""

from pydantic import BaseModel, Field


class ScriptAIResponse(BaseModel):
    """Structured response returned by Gemini."""

    title: str = Field(..., description="Video title")

    hook: str = Field(..., description="Opening hook")

    script: str = Field(..., description="Main script")

    hashtags: list[str] = Field(
        default_factory=list,
        description="Relevant hashtags",
    )