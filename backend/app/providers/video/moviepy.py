"""
MoviePy video provider.
"""

from pathlib import Path
from typing import Any

from moviepy import (
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
)

from app.providers.video.base import BaseVideoProvider


class MoviePyVideoProvider(BaseVideoProvider):
    """MoviePy implementation of the video provider."""

    @property
    def provider_name(self) -> str:
        return "moviepy"

    async def generate(
        self,
        image_paths: list[str],
        audio_path: str,
        output_path: Path,
        **kwargs: Any,
    ) -> Path:
        """
        Generate a video from images and audio.

        Returns:
            Path to the generated video.
        """

        if not image_paths:
            raise ValueError(
                "At least one image is required."
            )

        audio_clip = AudioFileClip(audio_path)

        try:
            duration_per_image = (
                audio_clip.duration / len(image_paths)
            )

            clips: list[ImageClip] = []

            for image_path in image_paths:
                clip = (
                    ImageClip(image_path)
                    .with_duration(duration_per_image)
                )

                clips.append(clip)

            video = concatenate_videoclips(
                clips,
                method="compose",
            )

            try:
                video = video.with_audio(audio_clip)

                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                video.write_videofile(
                    str(output_path),
                    codec="libx264",
                    audio_codec="aac",
                    fps=30,
                    logger=None,
                )

            finally:
                video.close()

        finally:
            audio_clip.close()

        return output_path

    async def health_check(
        self,
    ) -> bool:
        """
        Verify MoviePy is available.
        """

        return True