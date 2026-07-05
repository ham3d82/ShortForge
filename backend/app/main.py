"""
FastAPI application entrypoint.

Initializes the application, configures middleware,
registers routes, and sets up exception handlers.
"""

import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.cors import configure_cors
from app.middleware.request_id import RequestIDMiddleware

# Configure logging before anything else
configure_logging()

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url=f"{settings.API_V1_PREFIX}/docs" if settings.DEBUG else None,
        redoc_url=None,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json" if settings.DEBUG else None,
    )

    app.add_middleware(RequestIDMiddleware)

    configure_cors(app)

    register_exception_handlers(app)

    app.include_router(
        api_router,
        prefix=settings.API_V1_PREFIX,
    )

    # Serve generated images
    app.mount(
        "/generated_images",
        StaticFiles(directory=settings.GENERATED_IMAGES_DIR),
        name="generated_images",
    )

    logger.info(
        "Application initialized",
        extra={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
        },
    )

    return app


app = create_application()


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Application shutting down")