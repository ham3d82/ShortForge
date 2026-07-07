"""
Google Text-to-Speech provider.
"""

from io import BytesIO

from gtts import gTTS

from app.providers.speech.base import BaseSpeechProvider


class GTTSSpeechProvider(BaseSpeechProvider):
    """
    Google Text-to-Speech implementation.
    """

    async def generate(
        self,
        text: str,
        language: str,
    ) -> bytes:
        """
        Generate speech audio from text.
        """

        audio_buffer = BytesIO()

        tts = gTTS(
            text=text,
            lang=language,
        )

        tts.write_to_fp(audio_buffer)

        return audio_buffer.getvalue()