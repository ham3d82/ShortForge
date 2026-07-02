"""
CORS middleware configuration.

Configures Cross-Origin Resource Sharing for development.
Allows frontend development servers to access the API.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

logger = logging.getLogger(__name__)


def configure_cors(app: FastAPI) -> None:
    """Configure CORS middleware on the FastAPI application.

    In development, allows configured origins with credentials.
    In production, this should be restricted to known origins.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.debug(
        "CORS configured",
        extra={"origins": settings.CORS_ORIGINS},
    )