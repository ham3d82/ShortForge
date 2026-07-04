"""
Repository responsible for all GeneratedImage database operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.generated_image import GeneratedImage


class GeneratedImageRepository:
    """Handles CRUD operations for generated images."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        image: GeneratedImage,
    ) -> GeneratedImage:
        """
        Save a generated image.
        """
        self.db.add(image)

        await self.db.commit()
        await self.db.refresh(image)

        return image

    async def create_many(
        self,
        images: list[GeneratedImage],
    ) -> list[GeneratedImage]:
        """
        Save multiple generated images.
        """
        self.db.add_all(images)

        await self.db.commit()

        for image in images:
            await self.db.refresh(image)

        return images

    async def get_by_project_id(
        self,
        project_id: int,
    ) -> list[GeneratedImage]:
        """
        Return all generated images for a project.
        """
        stmt = (
            select(GeneratedImage)
            .where(GeneratedImage.project_id == project_id)
            .order_by(GeneratedImage.order)
        )

        result = await self.db.scalars(stmt)

        return list(result)

    async def delete_by_project_id(
        self,
        project_id: int,
    ) -> None:
        """
        Delete all generated images for a project.
        """
        images = await self.get_by_project_id(project_id)

        for image in images:
            await self.db.delete(image)

        await self.db.commit()