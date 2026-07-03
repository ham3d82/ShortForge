"""
Script dependencies.
"""

from app.dependencies.ai import get_ai_service
from app.services.script_service import ScriptService


def get_script_service() -> ScriptService:
    """Return a script service instance."""

    ai_service = get_ai_service()

    return ScriptService(ai_service)