"""
Centralized logging configuration.

Provides structured console logging for development.
No external logging services are configured.
"""

import contextvars
import logging
import sys

from app.core.config import settings

# Context variable to hold the unique request ID for the current async task
request_id_contextvar = contextvars.ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    """Logging filter that injects the current request ID from context into the log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_contextvar.get()
        return True


def configure_logging() -> None:
    """Configure application-wide logging.

    Sets up console logging with the configured log level.
    All loggers inherit from the root configuration.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | [req_id: %(request_id)s] | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.addFilter(RequestIDFilter())
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configured",
        extra={
            "level": settings.LOG_LEVEL,
            "app_name": settings.APP_NAME,
            "environment": settings.ENVIRONMENT,
        },
    )