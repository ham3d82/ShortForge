"""
Repository responsible for all GeneratedAudio database operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.generated_audio import GeneratedAudio


class GeneratedAudioRepository:
    """Handles CRUD operations for generated audio."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        audio: GeneratedAudio,
    ) -> GeneratedAudio:
        """
        Save generated audio.
        """
        self.db.add(audio)

        await self.db.commit()
        await self.db.refresh(audio)

        return audio

    async def get_by_project_id(
        self,
        project_id: int,
    ) -> list[GeneratedAudio]:
        """
        Return all generated audio for a project.
        """
        stmt = (
            select(GeneratedAudio)
            .where(
                GeneratedAudio.project_id == project_id,
            )
            .order_by(
                GeneratedAudio.created_at,
            )
        )

        result = await self.db.scalars(stmt)

        return list(result)

    async def delete_by_project_id(
        self,
        project_id: int,
    ) -> None:
        """
        Delete all generated audio for a project.
        """
        audio_files = await self.get_by_project_id(
            project_id,
        )

        for audio in audio_files:
            await self.db.delete(audio)

        await self.db.commit()