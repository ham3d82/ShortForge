"""
Repository responsible for all GeneratedVideo database operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.generated_video import GeneratedVideo


class GeneratedVideoRepository:
    """Handles CRUD operations for generated videos."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        video: GeneratedVideo,
    ) -> GeneratedVideo:
        """
        Save a generated video.
        """
        self.db.add(video)

        await self.db.commit()
        await self.db.refresh(video)

        return video

    async def get_by_project_id(
        self,
        project_id: int,
    ) -> GeneratedVideo | None:
        """
        Return the generated video for a project.
        """
        stmt = (
            select(GeneratedVideo)
            .where(
                GeneratedVideo.project_id == project_id,
            )
        )

        return await self.db.scalar(stmt)

    async def delete_by_project_id(
        self,
        project_id: int,
    ) -> None:
        """
        Delete the generated video for a project.
        """
        video = await self.get_by_project_id(
            project_id,
        )

        if video is None:
            return

        await self.db.delete(video)

        await self.db.commit()