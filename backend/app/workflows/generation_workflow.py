"""
Workflow responsible for generating a complete project.
"""

from app.schemas.generation import ProjectGenerationResponse
from app.schemas.project import ProjectResponse
from app.schemas.script import ScriptGenerateRequest

from app.services.image_service import ImageService
from app.services.script_service import ScriptService
from app.services.speech_service import SpeechService


class GenerationWorkflow:
    """
    Coordinates the complete content generation process.
    """

    def __init__(
        self,
        script_service: ScriptService,
        image_service: ImageService,
        speech_service: SpeechService,
    ) -> None:
        self.script_service = script_service
        self.image_service = image_service
        self.speech_service = speech_service

    async def generate(
        self,
        request: ScriptGenerateRequest,
    ) -> ProjectGenerationResponse:
        """
        Generate a complete project.
        """

        project = await self.script_service.generate(
            request,
        )

        image_result = await self.image_service.generate(
            project_id=project.id,
        )

        speech_result = await self.speech_service.generate(
            project_id=project.id,
        )

        return ProjectGenerationResponse(
            project=ProjectResponse.model_validate(
                project,
            ),
            images=image_result.images,
            audio=speech_result.audio,
        )