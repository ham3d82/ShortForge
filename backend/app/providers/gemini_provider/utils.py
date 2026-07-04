"""
Shared utilities for Gemini provider.
"""

import asyncio
from typing import Any

from google.genai.errors import ServerError


async def execute_with_retry(
    func,
    *args: Any,
    retries: int = 3,
    delay: int = 2,
    **kwargs: Any,
):
    """
    Execute a Gemini request with automatic retry on server errors.
    """

    last_error = None

    for attempt in range(retries):
        try:
            return func(*args, **kwargs)

        except ServerError as exc:
            last_error = exc

            if attempt == retries - 1:
                raise

            await asyncio.sleep(delay)

    raise last_error