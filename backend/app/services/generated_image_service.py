"""
Business logic for GeneratedImage operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.generated_image import GeneratedImage
from app.repositories.generated_image_repository import (
    GeneratedImageRepository,
)


class GeneratedImageService:
    """Handles generated image business logic."""

    def __init__(self, db: AsyncSession):
        self.repository = GeneratedImageRepository(db)

    async def create(
        self,
        project_id: int,
        prompt: str,
        image_url: str,
        order: int,
    ) -> GeneratedImage:
        """
        Create a generated image.
        """

        image = GeneratedImage(
            project_id=project_id,
            prompt=prompt,
            image_url=image_url,
            order=order,
        )

        return await self.repository.create(image)

    async def create_many(
        self,
        project_id: int,
        images: list[dict],
    ) -> list[GeneratedImage]:
        """
        Create multiple generated images.
        """

        objects = [
            GeneratedImage(
                project_id=project_id,
                prompt=image["prompt"],
                image_url=image["image_url"],
                order=image["order"],
            )
            for image in images
        ]

        return await self.repository.create_many(objects)

    async def get_by_project_id(
        self,
        project_id: int,
    ) -> list[GeneratedImage]:
        """
        Return all generated images for a project.
        """

        return await self.repository.get_by_project_id(project_id)

    async def delete_by_project_id(
        self,
        project_id: int,
    ) -> None:
        """
        Delete all generated images for a project.
        """

        await self.repository.delete_by_project_id(project_id)