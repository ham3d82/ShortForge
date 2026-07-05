"""
FastAPI application entrypoint.

Initializes the application, configures middleware,
registers routes, and sets up exception handlers.
"""

import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.cors import configure_cors
from app.middleware.request_id import RequestIDMiddleware

print("========== IMPORTS FINISHED ==========")

# Configure logging before anything else
configure_logging()

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    print("1 - create_application")

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url=f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else None,
        redoc_url=None,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json" if settings.DEBUG else None,
    )

    print("2 - FastAPI created")

    app.add_middleware(RequestIDMiddleware)

    print("3 - RequestID middleware added")

    configure_cors(app)

    print("4 - CORS configured")

    register_exception_handlers(app)

    print("5 - Exception handlers registered")

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    print("6 - Routers registered")

    logger.info(
        "Application initialized",
        extra={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
        },
    )

    print("7 - Returning app")

    return app


app = create_application()

print("8 - App instance created")


@app.on_event("startup")
async def startup_event() -> None:
    print("9 - Startup event")
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    print("10 - Shutdown event")
    logger.info("Application shutting down")