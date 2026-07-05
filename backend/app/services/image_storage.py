"""
Image storage service.

Handles saving generated images to disk.
"""

from pathlib import Path
from uuid import uuid4

from app.core.config import settings


class ImageStorageService:
    """Handles storing generated images on disk."""

    def __init__(self) -> None:
        self.output_dir: Path = settings.GENERATED_IMAGES_DIR
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save_image(
        self,
        image_bytes: bytes,
        extension: str = "png",
    ) -> str:
        """
        Save image bytes to disk.

        Returns:
            Relative image URL path.
        """

        filename = f"{uuid4().hex}.{extension}"

        file_path = self.output_dir / filename

        file_path.write_bytes(image_bytes)

        return f"/generated_images/{filename}"