"""
Script generation service.
"""

from app.prompts.script_prompt import build_script_prompt
from app.schemas.project import ProjectCreate
from app.schemas.script import (
    ScriptGenerateRequest,
    ScriptGenerateResponse,
)
from app.services.ai_service import AIService
from app.services.project_service import ProjectService


class ScriptService:
    """Service responsible for generating scripts."""

    def __init__(
        self,
        ai: AIService,
        project_service: ProjectService,
    ) -> None:
        self.ai = ai
        self.project_service = project_service

    async def generate(
        self,
        request: ScriptGenerateRequest,
    ):
        """Generate a short-form video script and save it."""

        prompt = build_script_prompt(
            topic=request.topic,
            language=request.language,
            duration=request.duration,
            tone=request.tone,
        )

        result: ScriptGenerateResponse = await self.ai.generate_structured(
            prompt=prompt,
            schema=ScriptGenerateResponse,
        )

        project = ProjectCreate(
            topic=request.topic,
            language=request.language,
            duration=request.duration,
            tone=request.tone,
            status="script_generated",
            title=result.title,
            hook=result.hook,
            script=result.script,
            hashtags=result.hashtags,
            thumbnail_prompt=result.thumbnail_prompt,
            image_prompts=result.image_prompts,
        )

        return await self.project_service.create(project)