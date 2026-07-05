"""
AI routes.
"""

from fastapi import APIRouter, Depends

from app.dependencies.ai import get_ai_service
from app.schemas.ai import (
    GenerateImageRequest,
    GenerateImageResponse,
    GenerateRequest,
    GenerateResponse,
)
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/health")
async def ai_health(
    ai: AIService = Depends(get_ai_service),
):
    """Check AI provider health."""

    return {
        "text_provider": ai.text_provider.provider_name,
        "image_provider": ai.image_provider.provider_name,
        "healthy": await ai.health_check(),
    }


@router.post(
    "/generate",
    response_model=GenerateResponse,
)
async def generate_text(
    request: GenerateRequest,
    ai: AIService = Depends(get_ai_service),
) -> GenerateResponse:
    """Generate text."""

    text = await ai.generate(request.prompt)

    return GenerateResponse(
        text=text,
    )


@router.post(
    "/generate-image",
    response_model=GenerateImageResponse,
)
async def generate_image(
    request: GenerateImageRequest,
    ai: AIService = Depends(get_ai_service),
) -> GenerateImageResponse:
    """Generate an image."""

    image_url = await ai.generate_image(
        request.prompt,
    )

    return GenerateImageResponse(
        image_url=image_url,
    )