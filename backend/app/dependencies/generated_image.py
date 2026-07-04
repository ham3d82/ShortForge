"""
Generated image dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.generated_image_service import GeneratedImageService


def get_generated_image_service(
    db: AsyncSession = Depends(get_db),
) -> GeneratedImageService:
    """
    Return a GeneratedImageService instance.
    """
    return GeneratedImageService(db)