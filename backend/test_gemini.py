import asyncio

from app.core.config import settings
from providers.gemini import GeminiProvider


async def main():
    print("API KEY:", repr(settings.GEMINI_API_KEY))
    print("MODEL:", settings.GEMINI_MODEL)

    provider = GeminiProvider()

    print("Health:", await provider.health_check())

    response = await provider.generate(
        "Say hello in one short sentence."
    )

    print("Response:", response)


if __name__ == "__main__":
    asyncio.run(main())