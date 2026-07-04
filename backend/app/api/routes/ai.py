"""
AI routes.
"""

from fastapi import APIRouter, Depends

from app.dependencies.ai import get_ai_service
from app.schemas.ai import GenerateRequest, GenerateResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/health")
async def ai_health(
    ai: AIService = Depends(get_ai_service),
):
    return {
        "provider": ai.text_provider.provider_name,
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
    """Generate text using the configured text provider."""

    text = await ai.generate(request.prompt)

    return GenerateResponse(text=text)