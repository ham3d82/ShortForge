"""
Schemas for GeneratedImage operations.
"""

from datetime import datetime

from pydantic import BaseModel


class GeneratedImageCreate(BaseModel):
    """Data required to create a generated image."""

    project_id: int
    prompt: str
    image_url: str
    order: int


class GeneratedImageResponse(BaseModel):
    """Generated image returned by the API."""

    id: int

    project_id: int

    prompt: str

    image_url: str

    order: int

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }