"""
Script dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.ai import get_ai_service
from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.services.script_service import ScriptService


def get_script_service(
    db: AsyncSession = Depends(get_db),
) -> ScriptService:
    """
    Return a ScriptService instance.
    """

    ai_service: AIService = get_ai_service()

    return ScriptService(
        ai=ai_service,
        project_service=ProjectService(db),
    )