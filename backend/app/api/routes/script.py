"""
Script generation routes.
"""

from fastapi import APIRouter, Depends

from app.dependencies.script import get_script_service
from app.schemas.project import ProjectResponse
from app.schemas.script import ScriptGenerateRequest
from app.services.script_service import ScriptService

router = APIRouter(
    prefix="/script",
    tags=["Script"],
)


@router.post(
    "/generate",
    response_model=ProjectResponse,
)
async def generate_script(
    request: ScriptGenerateRequest,
    service: ScriptService = Depends(get_script_service),
) -> ProjectResponse:
    """Generate a short-form video script and save it."""

    return await service.generate(request)