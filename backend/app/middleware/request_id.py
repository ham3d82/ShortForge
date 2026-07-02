"""
Request ID and request lifecycle logging middleware.

Generates or reads X-Request-ID headers and sets logging context,
logging the request start, success, or failure.
"""

import logging
import time
import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import request_id_contextvar

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to assign a unique request ID to each request and log its lifecycle."""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Check for incoming Request ID, otherwise generate a new one
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Store in request.state for exception handlers to access
        request.state.request_id = request_id
        
        # Set request ID in context variable
        token = request_id_contextvar.set(request_id)
        
        start_time = time.perf_counter()
        
        # Log request start with structured fields
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
            },
        )
        
        try:
            response: Response = await call_next(request)
            process_time = time.perf_counter() - start_time
            
            # Inject X-Request-ID header into response
            response.headers["X-Request-ID"] = request_id
            
            # Log request completion with structured fields
            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration": process_time,
                },
            )
            return response
            
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            # Log request failure with structured fields
            logger.exception(
                "Request failed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration": process_time,
                },
            )
            raise exc
            
        finally:
            # Always reset the context variable back to its previous state
            request_id_contextvar.reset(token)
