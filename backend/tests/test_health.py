"""
Tests for the health check endpoint.
"""

from fastapi.testclient import TestClient

from app.main import create_application

app = create_application()
client = TestClient(app)


class TestHealthEndpoint:
    """Test suite for the /api/v1/health endpoint."""

    def test_health_returns_200(self):
        """GET /api/v1/health should return HTTP 200."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_returns_status_ok(self):
        """Response body should contain status: ok."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert data["status"] == "ok"

    def test_health_returns_version(self):
        """Response body should contain version string."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert "version" in data
        assert isinstance(data["version"], str)
        assert len(data["version"]) > 0

    def test_health_response_structure(self):
        """Response should contain exactly status and version fields."""
        response = client.get("/api/v1/health")
        data = response.json()
        assert set(data.keys()) == {"status", "version"}