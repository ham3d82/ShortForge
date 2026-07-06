"""
Complete project generation routes.
"""

from fastapi import APIRouter, Depends

from app.dependencies.generation import get_generation_workflow
from app.schemas.generation import ProjectGenerationResponse
from app.schemas.script import ScriptGenerateRequest
from app.workflows.generation_workflow import GenerationWorkflow

router = APIRouter(
    prefix="/generation",
    tags=["Generation"],
)


@router.post(
    "/generate",
    response_model=ProjectGenerationResponse,
)
async def generate_project(
    request: ScriptGenerateRequest,
    workflow: GenerationWorkflow = Depends(
        get_generation_workflow,
    ),
) -> ProjectGenerationResponse:
    """
    Generate a complete project.
    """

    return await workflow.generate(request)