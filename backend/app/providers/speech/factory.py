"""
Speech provider factory.
"""

from app.core.config import settings
from app.providers.speech.base import BaseSpeechProvider
from app.providers.speech.gtts import GTTSSpeechProvider


def get_speech_provider() -> BaseSpeechProvider:
    """
    Return the configured speech provider.
    """

    provider = settings.SPEECH_PROVIDER.lower()

    providers: dict[str, BaseSpeechProvider] = {
        "gtts": GTTSSpeechProvider(),
    }

    try:
        return providers[provider]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported speech provider: {provider}",
        ) from exc