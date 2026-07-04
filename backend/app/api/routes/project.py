"""
Project routes.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.dependencies.project import get_project_service
from app.schemas.project import (
    ProjectResponse,
    ProjectStatusUpdate,
)
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get(
    "",
    response_model=list[ProjectResponse],
)
async def list_projects(
    service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    """
    Return all projects.
    """

    return await service.list()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """
    Return a project by its ID.
    """

    project = await service.get_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.patch(
    "/{project_id}/status",
    response_model=ProjectResponse,
)
async def update_project_status(
    project_id: int,
    data: ProjectStatusUpdate,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """
    Update project status.
    """

    project = await service.get_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return await service.update_status(project, data)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
) -> None:
    """
    Delete a project.
    """

    project = await service.get_by_id(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    await service.delete(project)