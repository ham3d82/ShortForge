"""
Generation workflow dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.ai import get_ai_service
from app.dependencies.image import get_generated_image_service
from app.dependencies.project import get_project_service
from app.dependencies.script import get_script_service
from app.services.generated_image_service import GeneratedImageService
from app.services.image_service import ImageService
from app.services.project_service import ProjectService
from app.services.script_service import ScriptService
from app.workflows.generation_workflow import GenerationWorkflow


def get_generation_workflow(
    db: AsyncSession = Depends(get_db),
    ai=Depends(get_ai_service),
    project_service: ProjectService = Depends(get_project_service),
    generated_image_service: GeneratedImageService = Depends(
        get_generated_image_service,
    ),
) -> GenerationWorkflow:
    """
    Return the application generation workflow.
    """

    script_service = ScriptService(
        ai=ai,
        project_service=project_service,
    )

    image_service = ImageService(ai=ai)

    return GenerationWorkflow(
        script_service=script_service,
        project_service=project_service,
        image_service=image_service,
        generated_image_service=generated_image_service,
    )