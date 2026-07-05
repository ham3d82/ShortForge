"""
Generation workflow dependencies.
"""

from fastapi import Depends

from app.dependencies.image import get_image_service
from app.dependencies.script import get_script_service

from app.services.image_service import ImageService
from app.services.script_service import ScriptService

from app.workflows.generation_workflow import GenerationWorkflow


def get_generation_workflow(
    script_service: ScriptService = Depends(get_script_service),
    image_service: ImageService = Depends(get_image_service),
) -> GenerationWorkflow:
    """
    Return the application generation workflow.
    """

    return GenerationWorkflow(
        script_service=script_service,
        image_service=image_service,
    )