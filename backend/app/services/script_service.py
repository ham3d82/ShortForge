"""
Script generation service.
"""

from app.prompts.script_prompt import build_script_prompt
from app.schemas.script import (
    ScriptGenerateRequest,
    ScriptGenerateResponse,
)
from app.services.ai_service import AIService


class ScriptService:
    """Service responsible for generating scripts."""

    def __init__(
        self,
        ai: AIService,
    ) -> None:
        self.ai = ai

    async def generate(
        self,
        request: ScriptGenerateRequest,
    ) -> ScriptGenerateResponse:
        """Generate a short-form video script."""

        prompt = build_script_prompt(
            topic=request.topic,
            language=request.language,
            duration=request.duration,
            tone=request.tone,
        )

        result = await self.ai.generate_structured(
            prompt=prompt,
            schema=ScriptGenerateResponse,
        )

        return result