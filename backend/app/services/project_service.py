"""
Business logic for Project operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import (
    ProjectCreate,
    ProjectStatusUpdate,
)


class ProjectService:
    """Handles project business logic."""

    def __init__(self, db: AsyncSession):
        self.repository = ProjectRepository(db)

    async def create(self, data: ProjectCreate) -> Project:
        """
        Create and persist a new project.
        """

        project = Project(
            topic=data.topic,
            language=data.language,
            duration=data.duration,
            tone=data.tone,
            status=data.status,
            title=data.title,
            hook=data.hook,
            script=data.script,
            hashtags=data.hashtags,
            thumbnail_prompt=data.thumbnail_prompt,
            image_prompts=data.image_prompts,
        )

        return await self.repository.create(project)

    async def get_by_id(
        self,
        project_id: int,
    ) -> Project | None:
        """
        Get a project by its ID.
        """
        return await self.repository.get_by_id(project_id)

    async def list(self) -> list[Project]:
        """
        Return all projects.
        """
        return await self.repository.list()

    async def delete(
        self,
        project: Project,
    ) -> None:
        """
        Delete a project.
        """
        await self.repository.delete(project)

    async def update(
        self,
        project: Project,
    ) -> Project:
        """
        Persist pending changes.
        """
        return await self.repository.update(project)

    async def update_status(
        self,
        project: Project,
        data: ProjectStatusUpdate,
    ) -> Project:
        """
        Update project status.
        """

        project.status = data.status

        return await self.repository.update(project)