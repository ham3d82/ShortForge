"""
Script generation routes.
"""

from fastapi import APIRouter, Depends

from app.dependencies.script import get_script_service
from app.schemas.script import (
    ScriptGenerateRequest,
    ScriptGenerateResponse,
)
from app.services.script_service import ScriptService

router = APIRouter(
    prefix="/script",
    tags=["Script"],
)


@router.post(
    "/generate",
    response_model=ScriptGenerateResponse,
)
async def generate_script(
    request: ScriptGenerateRequest,
    service: ScriptService = Depends(get_script_service),
) -> ScriptGenerateResponse:
    """Generate a short-form video script."""

    return await service.generate(request)