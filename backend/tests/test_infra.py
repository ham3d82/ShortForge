"""
Tests for infrastructure, middleware, and exception handling.
"""

from fastapi import APIRouter
from fastapi.testclient import TestClient
import pytest
from pydantic import ValidationError

from app.main import create_application
from app.core.exceptions import AppException
from app.core.config import Settings

# Create a fresh app for infra/middleware tests
app = create_application()

# We can register some test endpoints specifically for verifying exception handling
test_router = APIRouter()


@test_router.get("/test/app-exception")
async def trigger_app_exception():
    raise AppException(status_code=400, detail="This is a test AppException")


@test_router.get("/test/unhandled-exception")
async def trigger_unhandled_exception():
    raise ValueError("This is a test unexpected error")


app.include_router(test_router)
client = TestClient(app, raise_server_exceptions=False)


class TestRequestIDMiddleware:
    """Test suite for Request ID Middleware."""

    def test_request_id_in_response_headers(self):
        """Responses should include a generated X-Request-ID header."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0

    def test_request_id_custom_header(self):
        """If X-Request-ID is sent in requests, it should be propagated to the response."""
        custom_id = "test-custom-request-id-1234"
        response = client.get("/api/v1/health", headers={"X-Request-ID": custom_id})
        assert response.status_code == 200
        assert response.headers["X-Request-ID"] == custom_id


class TestExceptionHandlingSchema:
    """Test suite for standard exception handling and error schema."""

    def test_not_found_standard_schema(self):
        """A 404 error should return the standardized JSON error schema."""
        response = client.get("/api/v1/does-not-exist")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert "request_id" in data["error"]
        # Code should correspond to the type of exception (e.g., HTTP_EXCEPTION)
        assert data["error"]["code"] == "HTTP_EXCEPTION"
        assert len(data["error"]["request_id"]) > 0

    def test_app_exception_standard_schema(self):
        """An AppException should return the standardized JSON error schema with custom details."""
        response = client.get("/test/app-exception")
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "AppException"
        assert data["error"]["message"] == "This is a test AppException"
        assert "request_id" in data["error"]

    def test_unhandled_exception_standard_schema(self):
        """An unhandled Exception should return INTERNAL_ERROR code and the standardized JSON schema."""
        response = client.get("/test/unhandled-exception")
        assert response.status_code == 500
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "INTERNAL_ERROR"
        assert data["error"]["message"] == "An unexpected error occurred"
        assert "request_id" in data["error"]


class TestConfigValidation:
    """Test suite for configuration validation."""

    def test_invalid_environment_raises_validation_error(self):
        """Initializing settings with an invalid ENVIRONMENT should raise a ValidationError."""
        with pytest.raises(ValidationError):
            Settings(ENVIRONMENT="invalid_env")

    def test_invalid_log_level_raises_validation_error(self):
        """Initializing settings with an invalid LOG_LEVEL should raise a ValidationError."""
        with pytest.raises(ValidationError):
            Settings(LOG_LEVEL="TRACE")

    def test_invalid_port_raises_validation_error(self):
        """Initializing settings with an invalid PORT should raise a ValidationError."""
        with pytest.raises(ValidationError):
            Settings(PORT=999999)
