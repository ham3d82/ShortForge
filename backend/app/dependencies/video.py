"""
Video dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies.ai import get_ai_service
from app.dependencies.image import get_image_service
from app.dependencies.project import get_project_service

from app.repositories.generated_audio_repository import (
    GeneratedAudioRepository,
)
from app.repositories.generated_video_repository import (
    GeneratedVideoRepository,
)

from app.services.ai_service import AIService
from app.services.generated_image_service import (
    GeneratedImageService,
)
from app.services.project_service import ProjectService
from app.services.video_service import VideoService
from app.services.video_storage import (
    VideoStorageService,
)


def get_video_service(
    db: AsyncSession = Depends(get_db),
) -> VideoService:
    """
    Return a VideoService instance.
    """

    ai_service: AIService = get_ai_service()

    project_service: ProjectService = (
        get_project_service(db)
    )

    image_service: GeneratedImageService = (
        get_image_service(db)
    )

    audio_repository = GeneratedAudioRepository(
        db,
    )

    video_repository = GeneratedVideoRepository(
        db,
    )

    storage = VideoStorageService()

    return VideoService(
        ai=ai_service,
        project_service=project_service,
        image_service=image_service,
        audio_repository=audio_repository,
        repository=video_repository,
        storage=storage,
    )