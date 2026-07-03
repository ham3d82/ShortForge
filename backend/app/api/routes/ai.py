"""
AI routes.
"""

from fastapi import APIRouter, Depends

from app.dependencies.ai import get_ai_service
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/health")
async def ai_health(
    ai: AIService = Depends(get_ai_service),
):
    return {
        "provider": ai.provider.provider_name,
        "healthy": await ai.health_check(),
    }