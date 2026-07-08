"""
Schemas for GeneratedVideo operations.
"""

from datetime import datetime

from pydantic import BaseModel


class GeneratedVideoCreate(BaseModel):
    """Data required to create a generated video."""

    project_id: int

    video_url: str

    duration: float

    resolution: str

    provider: str


class GeneratedVideoResponse(BaseModel):
    """Generated video returned by the API."""

    id: int

    project_id: int

    video_url: str

    duration: float

    resolution: str

    provider: str

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class GenerateVideoRequest(BaseModel):
    """Request to generate a project video."""

    project_id: int


class GenerateVideoResponse(BaseModel):
    """Response returned after generating project video."""

    project_id: int

    status: str

    video: GeneratedVideoResponse