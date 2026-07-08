"""
Video generation service.
"""

from pathlib import Path

from app.db.models.generated_video import GeneratedVideo
from app.repositories.generated_audio_repository import (
    GeneratedAudioRepository,
)
from app.repositories.generated_video_repository import (
    GeneratedVideoRepository,
)
from app.schemas.generated_video import (
    GenerateVideoResponse,
    GeneratedVideoResponse,
)
from app.schemas.project import ProjectStatusUpdate
from app.services.ai_service import AIService
from app.services.generated_image_service import (
    GeneratedImageService,
)
from app.services.project_service import ProjectService
from app.services.video_storage import (
    VideoStorageService,
)


class VideoService:
    """Service responsible for generating videos."""

    def __init__(
        self,
        ai: AIService,
        project_service: ProjectService,
        image_service: GeneratedImageService,
        audio_repository: GeneratedAudioRepository,
        repository: GeneratedVideoRepository,
        storage: VideoStorageService,
    ) -> None:
        self.ai = ai
        self.project_service = project_service
        self.image_service = image_service
        self.audio_repository = audio_repository
        self.repository = repository
        self.storage = storage

    async def generate(
        self,
        project_id: int,
    ) -> GenerateVideoResponse:
        """
        Generate a video for a project.
        """

        project = await self.project_service.get_by_id(
            project_id,
        )

        if project is None:
            raise ValueError(
                "Project not found.",
            )

        images = await self.image_service.get_by_project_id(
            project_id,
        )

        if not images:
            raise ValueError(
                "No generated images found.",
            )

        audio_files = await self.audio_repository.get_by_project_id(
            project_id,
        )

        if not audio_files:
            raise ValueError(
                "No generated audio found.",
            )

        image_paths = [
            str(
                Path(image.image_url.lstrip("/"))
            )
            for image in images
        ]

        audio_path = str(
            Path(
                audio_files[0].audio_url.lstrip("/")
            )
        )

        output_path = await self.storage.create_output_path()

        video_path = await self.ai.generate_video(
            image_paths=image_paths,
            audio_path=audio_path,
            output_path=output_path,
        )

        generated_video = GeneratedVideo(
            project_id=project.id,
            video_url=self.storage.get_video_url(
                video_path,
            ),
            duration=float(project.duration),
            resolution="1080x1920",
            provider="moviepy",
        )

        generated_video = await self.repository.create(
            generated_video,
        )

        await self.project_service.update_status(
            project,
            ProjectStatusUpdate(
                status="video_generated",
            ),
        )

        return GenerateVideoResponse(
            project_id=project.id,
            status="video_generated",
            video=GeneratedVideoResponse.model_validate(
                generated_video,
            ),
        )