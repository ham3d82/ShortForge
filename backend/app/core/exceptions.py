"""
Global exception definitions and handlers.

Defines application-specific exception classes and
registers global exception handlers with FastAPI.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import request_id_contextvar

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base application exception with status code and detail."""

    def __init__(self, status_code: int = 500, detail: str = "Internal server error"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ValidationException(AppException):
    """Validation error."""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=422, detail=detail)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI application."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        request_id = getattr(
    request.state,
    "request_id",
    request_id_contextvar.get(),
)
        logger.warning(
            "Application exception",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "path": str(request.url),
                "request_id": request_id,
            },
        )
        error_content = {
            "error": {
                "code": exc.__class__.__name__,
                "message": exc.detail,
            }
        }
        if request_id and request_id != "-":
            error_content["error"]["request_id"] = request_id

        return JSONResponse(
            status_code=exc.status_code,
            content=error_content,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        request_id = getattr(
    request.state,
    "request_id",
    request_id_contextvar.get(),
)
        logger.warning(
            "HTTP exception",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "path": str(request.url),
                "request_id": request_id,
            },
        )
        error_content = {
            "error": {
                "code": "HTTP_EXCEPTION",
                "message": exc.detail,
            }
        }
        if request_id and request_id != "-":
            error_content["error"]["request_id"] = request_id

        return JSONResponse(
            status_code=exc.status_code,
            content=error_content,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        request_id = getattr(
    request.state,
    "request_id",
    request_id_contextvar.get(),
)
        logger.warning(
            "Request validation error",
            extra={
                "errors": exc.errors(),
                "path": str(request.url),
                "request_id": request_id,
            },
        )
        error_content = {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation error",
                "details": exc.errors(),
            }
        }
        if request_id and request_id != "-":
            error_content["error"]["request_id"] = request_id

        return JSONResponse(
            status_code=422,
            content=error_content,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(
    request.state,
    "request_id",
    request_id_contextvar.get(),
)
        logger.exception(
            "Unhandled exception",
            extra={
                "path": str(request.url),
                "request_id": request_id,
            },
        )
        error_content = {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            }
        }
        if request_id and request_id != "-":
            error_content["error"]["request_id"] = request_id

        return JSONResponse(
            status_code=500,
            content=error_content,
        )
