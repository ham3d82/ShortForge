"""
Speech storage service.

Handles saving generated audio files to disk.
"""

from pathlib import Path
from uuid import uuid4

from app.core.config import settings


class SpeechStorageService:
    """Handles storing generated audio files on disk."""

    def __init__(self) -> None:
        self.output_dir: Path = settings.GENERATED_AUDIO_DIR

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save_audio(
        self,
        audio_bytes: bytes,
        extension: str = "mp3",
    ) -> str:
        """
        Save audio bytes to disk.

        Returns:
            Relative audio URL path.
        """

        filename = f"{uuid4().hex}.{extension}"

        file_path = self.output_dir / filename

        file_path.write_bytes(audio_bytes)

        return f"/generated_audio/{filename}"