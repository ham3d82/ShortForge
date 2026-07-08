"""
Speech dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies.ai import get_ai_service
from app.dependencies.project import get_project_service

from app.repositories.generated_audio_repository import (
    GeneratedAudioRepository,
)

from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.services.speech_service import SpeechService
from app.services.speech_storage import (
    SpeechStorageService,
)


def get_speech_service(
    db: AsyncSession = Depends(get_db),
) -> SpeechService:
    """
    Return a SpeechService instance.
    """

    ai_service: AIService = get_ai_service()

    project_service: ProjectService = get_project_service(db)

    audio_repository = GeneratedAudioRepository(db)

    storage_service = SpeechStorageService()

    return SpeechService(
        ai=ai_service,
        project_service=project_service,
        audio_repository=audio_repository,
        storage=storage_service,
    )