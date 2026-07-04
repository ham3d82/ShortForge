"""
Schemas for Project operations.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """Data required to create a project."""

    topic: str
    language: str
    duration: int
    tone: str

    title: str
    hook: str
    script: str

    hashtags: list[str]

    thumbnail_prompt: str

    image_prompts: list[str]

    status: str = "script_generated"


class ProjectResponse(BaseModel):
    """Project returned by the API."""

    id: int

    topic: str
    language: str
    duration: int
    tone: str

    status: str

    title: str
    hook: str
    script: str

    hashtags: list[str]

    thumbnail_prompt: str

    image_prompts: list[str]

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }