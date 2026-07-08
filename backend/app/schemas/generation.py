"""
Schemas for complete project generation.
"""

from pydantic import BaseModel

from app.schemas.generated_audio import (
    GeneratedAudioResponse,
)
from app.schemas.generated_image import (
    GeneratedImageResponse,
)
from app.schemas.generated_video import (
    GeneratedVideoResponse,
)
from app.schemas.project import ProjectResponse


class ProjectGenerationResponse(BaseModel):
    """
    Response returned after generating a complete project.
    """

    project: ProjectResponse

    images: list[GeneratedImageResponse]

    audio: GeneratedAudioResponse

    video: GeneratedVideoResponse