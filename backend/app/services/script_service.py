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

    def __init__(self) -> None:
        self.ai = AIService()

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

        result = await self.ai.generate(prompt)

        return self._parse_response(result)

    def _parse_response(
        self,
        text: str,
    ) -> ScriptGenerateResponse:
        """Parse the AI response into a structured object."""

        title = ""
        hook = ""
        script = ""
        hashtags = []

        current = None

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            upper = line.upper()

            if upper.startswith("TITLE:"):
                current = "title"
                value = line[6:].strip()
                if value:
                    title = value
                continue

            if upper.startswith("HOOK:"):
                current = "hook"
                value = line[5:].strip()
                if value:
                    hook += value + " "
                continue

            if upper.startswith("SCRIPT:"):
                current = "script"
                value = line[7:].strip()
                if value:
                    script += value + "\n"
                continue

            if upper.startswith("HASHTAGS:"):
                current = "hashtags"
                value = line[9:].strip()
                if value:
                    hashtags.extend(value.split())
                continue

            if current == "title":
                title += line + " "

            elif current == "hook":
                hook += line + " "

            elif current == "script":
                script += line + "\n"

            elif current == "hashtags":
                hashtags.extend(line.split())

        return ScriptGenerateResponse(
            title=title.strip(),
            hook=hook.strip(),
            script=script.strip(),
            hashtags=hashtags,
        )