"""
Speech generation service.
"""

from app.db.models.generated_audio import GeneratedAudio

from app.repositories.generated_audio_repository import (
    GeneratedAudioRepository,
)

from app.schemas.generated_audio import (
    GenerateSpeechResponse,
    GeneratedAudioResponse,
)

from app.schemas.project import ProjectStatusUpdate

from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.services.speech_storage import (
    SpeechStorageService,
)


class SpeechService:
    """Service responsible for generating speech for a project."""

    def __init__(
        self,
        ai: AIService,
        project_service: ProjectService,
        audio_repository: GeneratedAudioRepository,
        storage: SpeechStorageService,
    ) -> None:
        self.ai = ai
        self.project_service = project_service
        self.audio_repository = audio_repository
        self.storage = storage

    async def generate(
        self,
        project_id: int,
    ) -> GenerateSpeechResponse:
        """
        Generate speech audio for a project.
        """

        project = await self.project_service.get_by_id(
            project_id,
        )

        if project is None:
            raise ValueError(
                "Project not found.",
            )

        audio_bytes = await self.ai.generate_speech(
            text=project.script,
            language=project.language,
        )

        audio_url = await self.storage.save_audio(
            audio_bytes=audio_bytes,
        )

        generated_audio = GeneratedAudio(
            project_id=project.id,
            text=project.script,
            audio_url=audio_url,
            provider="gtts",
            language=project.language,
        )

        generated_audio = await self.audio_repository.create(
            generated_audio,
        )

        await self.project_service.update_status(
            project,
            ProjectStatusUpdate(
                status="speech_generated",
            ),
        )

        return GenerateSpeechResponse(
            project_id=project.id,
            status="speech_generated",
            audio=GeneratedAudioResponse.model_validate(
                generated_audio,
            ),
        )