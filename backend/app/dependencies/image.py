"""
Image dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies.ai import get_ai_service
from app.dependencies.project import get_project_service

from app.repositories.generated_image_repository import (
    GeneratedImageRepository,
)

from app.services.ai_service import AIService
from app.services.image_service import ImageService
from app.services.project_service import ProjectService


def get_image_service(
    db: AsyncSession = Depends(get_db),
) -> ImageService:
    """
    Return an ImageService instance.
    """

    ai_service: AIService = get_ai_service()

    project_service: ProjectService = get_project_service(db)

    image_repository = GeneratedImageRepository(db)

    return ImageService(
        ai=ai_service,
        project_service=project_service,
        image_repository=image_repository,
    )