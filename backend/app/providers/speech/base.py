"""
Base interface for speech providers.
"""

from abc import ABC, abstractmethod


class BaseSpeechProvider(ABC):
    """
    Abstract base class for all speech providers.

    Every speech provider must implement this interface.
    """

    @abstractmethod
    async def generate(
        self,
        text: str,
        language: str,
    ) -> bytes:
        """
        Generate speech audio from text.

        Args:
            text: The text to convert into speech.
            language: Language code (e.g. "en", "ar").

        Returns:
            Raw audio bytes.
        """
        raise NotImplementedError