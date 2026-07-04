"""
Schemas for generated images.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class GeneratedImageCreate(BaseModel):
    """Data required to create a generated image."""

    project_id: int

    prompt: str

    image_url: str

    order: int = Field(
        ge=1,
    )


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


class GenerateImagesRequest(BaseModel):
    """Request to generate images for a project."""

    project_id: int


class GenerateImagesResponse(BaseModel):
    """Response returned after generating project images."""

    project_id: int

    status: str

    images: list[GeneratedImageResponse]