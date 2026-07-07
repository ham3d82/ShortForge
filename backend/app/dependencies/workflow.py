"""
Workflow dependencies.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.dependencies.image import get_image_service
from app.dependencies.script import get_script_service
from app.dependencies.speech import get_speech_service

from app.services.image_service import ImageService
from app.services.script_service import ScriptService
from app.services.speech_service import SpeechService

from app.workflows.generation_workflow import (
    GenerationWorkflow,
)


def get_generation_workflow(
    db: AsyncSession = Depends(get_db),
) -> GenerationWorkflow:
    """
    Create the GenerationWorkflow instance.
    """

    script_service: ScriptService = get_script_service(
        db,
    )

    image_service: ImageService = get_image_service(
        db,
    )

    speech_service: SpeechService = get_speech_service(
        db,
    )

    return GenerationWorkflow(
        script_service=script_service,
        image_service=image_service,
        speech_service=speech_service,
    )