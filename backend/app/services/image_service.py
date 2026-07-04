"""
Image generation service.
"""

from app.db.models.generated_image import GeneratedImage
from app.schemas.image import (
    GenerateImagesResponse,
    GeneratedImageResponse,
)
from app.schemas.project import ProjectStatusUpdate
from app.services.ai_service import AIService
from app.services.project_service import ProjectService
from app.repositories.generated_image_repository import (
    GeneratedImageRepository,
)


class ImageService:
    """Service responsible for generating project images."""

    def __init__(
        self,
        ai: AIService,
        project_service: ProjectService,
        image_repository: GeneratedImageRepository,
    ) -> None:
        self.ai = ai
        self.project_service = project_service
        self.image_repository = image_repository

    async def generate(
        self,
        project_id: int,
    ) -> GenerateImagesResponse:
        """
        Generate all images for a project.
        """

        project = await self.project_service.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found.")

        generated_images: list[GeneratedImage] = []

        for index, prompt in enumerate(project.image_prompts, start=1):

            image_url = await self.ai.generate_image(prompt)

            image = GeneratedImage(
                project_id=project.id,
                prompt=prompt,
                image_url=image_url,
                order=index,
            )

            generated_images.append(image)

        generated_images = await self.image_repository.create_many(
            generated_images,
        )

        await self.project_service.update_status(
            project,
            ProjectStatusUpdate(
                status="images_generated",
            ),
        )

        return GenerateImagesResponse(
            project_id=project.id,
            status="images_generated",
            images=[
                GeneratedImageResponse.model_validate(image)
                for image in generated_images
            ],
        )