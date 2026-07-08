"""
Video generation endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.video import get_video_service
from app.schemas.generated_video import (
    GenerateVideoRequest,
    GenerateVideoResponse,
)
from app.services.video_service import VideoService

router = APIRouter(
    prefix="/video",
    tags=["Video"],
)


@router.post(
    "/generate",
    response_model=GenerateVideoResponse,
)
async def generate_video(
    request: GenerateVideoRequest,
    service: VideoService = Depends(
        get_video_service,
    ),
) -> GenerateVideoResponse:
    """
    Generate a video for a project.
    """

    try:
        return await service.generate(
            project_id=request.project_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc