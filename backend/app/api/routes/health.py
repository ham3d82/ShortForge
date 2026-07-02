"""
Health check endpoint.

Provides a simple health check for monitoring and load balancers.
Returns application status and version information.
"""

import logging

from fastapi import APIRouter

from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """Return application health status.

    Returns:
        dict: Status information including app name and version.
    """
    logger.debug("Health check requested")
    return {
        "status": "ok",
        "version": settings.APP_VERSION,
    }