"""
Workflow dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies.services import (
    get_generated_image_service,
    get_image_service,
    get_project_service,
    get_script_service,
)

from app.services.generated_image_service import GeneratedImageService
from app.services.image_service import ImageService
from app.services.project_service import ProjectService
from app.services.script_service import ScriptService

from app.workflows.generation_workflow import GenerationWorkflow


def get_generation_workflow(
    db: AsyncSession = Depends(get_db),
) -> GenerationWorkflow:
    """
    Create the GenerationWorkflow instance.
    """

    script_service: ScriptService = get_script_service(db)
    project_service: ProjectService = get_project_service(db)
    image_service: ImageService = get_image_service(db)
    generated_image_service: GeneratedImageService = (
        get_generated_image_service(db)
    )

    return GenerationWorkflow(
        script_service=script_service,
        project_service=project_service,
        image_service=image_service,
        generated_image_service=generated_image_service,
    )