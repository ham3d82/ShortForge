"""
Repository responsible for all Project database operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import Project


class ProjectRepository:
    """Handles CRUD operations for Project."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, project: Project) -> Project:
        """
        Create a new project.
        """
        self.db.add(project)

        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def get_by_id(
        self,
        project_id: int,
    ) -> Project | None:
        """
        Get a project by its ID.
        """
        stmt = select(Project).where(Project.id == project_id)

        return await self.db.scalar(stmt)

    async def list(self) -> list[Project]:
        """
        Return all projects ordered by newest first.
        """
        stmt = select(Project).order_by(Project.created_at.desc())

        result = await self.db.scalars(stmt)

        return list(result)

    async def delete(
        self,
        project: Project,
    ) -> None:
        """
        Delete a project.
        """
        await self.db.delete(project)
        await self.db.commit()

    async def update(self) -> None:
        """
        Commit pending changes.
        """
        await self.db.commit()