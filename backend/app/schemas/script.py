"""
Schemas for script generation.
"""

from pydantic import BaseModel, Field


class ScriptGenerateRequest(BaseModel):
    """Request for generating a short-form video script."""

    topic: str = Field(..., min_length=3, max_length=200)
    language: str = Field(default="en")
    duration: int = Field(default=60, ge=15, le=300)
    tone: str = Field(default="educational")


class ScriptGenerateResponse(BaseModel):
    """Generated script response."""

    title: str
    hook: str
    script: str
    hashtags: list[str]

    thumbnail_prompt: str

    image_prompts: list[str] = Field(
        min_length=4,
        max_length=8,
    )