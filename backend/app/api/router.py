"""
Centralized API router.

Aggregates all API routes and sub-routers of the application.
"""

from fastapi import APIRouter

from app.api.routes.ai import router as ai_router
from app.api.routes.generation import (
    router as generation_router,
)
from app.api.routes.health import router as health_router
from app.api.routes.project import router as project_router
from app.api.routes.script import router as script_router

api_router = APIRouter()

# Register routes
api_router.include_router(health_router, tags=["health"])
api_router.include_router(ai_router)
api_router.include_router(script_router)
api_router.include_router(project_router)
api_router.include_router(generation_router)