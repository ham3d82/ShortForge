"""
Video storage service.

Handles saving generated videos to disk.
"""

from pathlib import Path
from uuid import uuid4

from app.core.config import settings


class VideoStorageService:
    """Handles storing generated videos on disk."""

    def __init__(self) -> None:
        self.output_dir: Path = settings.GENERATED_VIDEOS_DIR

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def create_output_path(
        self,
        extension: str = "mp4",
    ) -> Path:
        """
        Create a unique output path for a generated video.

        Returns:
            Absolute output path.
        """

        filename = f"{uuid4().hex}.{extension}"

        return self.output_dir / filename

    def get_video_url(
        self,
        video_path: Path,
    ) -> str:
        """
        Convert a saved video path into a public URL.

        Returns:
            Relative video URL.
        """

        return (
            f"/generated_videos/{video_path.name}"
        )