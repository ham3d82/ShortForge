"""
Workflow responsible for generating a complete project.
"""

from app.schemas.script import (
    ScriptGenerateRequest,
    ScriptGenerateResponse,
)
from app.services.generated_image_service import GeneratedImageService
from app.services.image_service import ImageService
from app.services.project_service import ProjectService
from app.services.script_service import ScriptService


class GenerationWorkflow:
    """
    Coordinates the complete content generation process.
    """

    def __init__(
        self,
        script_service: ScriptService,
        project_service: ProjectService,
        image_service: ImageService,
        generated_image_service: GeneratedImageService,
    ) -> None:
        self.script_service = script_service
        self.project_service = project_service
        self.image_service = image_service
        self.generated_image_service = generated_image_service

    async def generate(
        self,
        request: ScriptGenerateRequest,
    ):
        """
        Generate a complete project.

        This implementation will grow gradually.
        """

        return await self.script_service.generate(request)