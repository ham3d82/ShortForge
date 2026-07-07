"""
Schemas for generated audio.
"""

from datetime import datetime

from pydantic import BaseModel


class GeneratedAudioCreate(BaseModel):
    """Data required to create generated audio."""

    project_id: int

    text: str

    audio_url: str

    provider: str

    language: str


class GeneratedAudioResponse(BaseModel):
    """Generated audio returned by the API."""

    id: int

    project_id: int

    text: str

    audio_url: str

    provider: str

    language: str

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class GenerateSpeechRequest(BaseModel):
    """Request to generate speech for a project."""

    project_id: int


class GenerateSpeechResponse(BaseModel):
    """Response returned after generating project speech."""

    project_id: int

    status: str

    audio: GeneratedAudioResponse