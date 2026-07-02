"""
Centralized API router.

Aggregates all API routes and sub-routers of the application.
"""

from fastapi import APIRouter

from app.api.routes.health import router as health_router

api_router = APIRouter()

# Register routes
api_router.include_router(health_router, tags=["health"])
