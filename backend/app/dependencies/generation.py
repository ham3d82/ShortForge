"""
Generation workflow dependencies.
"""

from fastapi import Depends

from app.dependencies.image import get_image_service
from app.dependencies.script import get_script_service
from app.dependencies.speech import get_speech_service
from app.dependencies.video import get_video_service

from app.services.image_service import ImageService
from app.services.script_service import ScriptService
from app.services.speech_service import SpeechService
from app.services.video_service import VideoService

from app.workflows.generation_workflow import GenerationWorkflow


def get_generation_workflow(
    script_service: ScriptService = Depends(
        get_script_service,
    ),
    image_service: ImageService = Depends(
        get_image_service,
    ),
    speech_service: SpeechService = Depends(
        get_speech_service,
    ),
    video_service: VideoService = Depends(
        get_video_service,
    ),
) -> GenerationWorkflow:
    """
    Return the application generation workflow.
    """

    return GenerationWorkflow(
        script_service=script_service,
        image_service=image_service,
        speech_service=speech_service,
        video_service=video_service,
    )