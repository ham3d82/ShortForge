"""
Script dependencies.
"""

from app.services.script_service import ScriptService


def get_script_service() -> ScriptService:
    """Return a script service instance."""
    return ScriptService()