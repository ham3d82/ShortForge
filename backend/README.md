# ShortForge Backend

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
cd backend

# Install dependencies
pip install -e ".[dev]"

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verify

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status": "ok", "version": "0.1.0"}
```

### Run Tests

```bash
pytest -v
```

## API Documentation

When running in development mode, interactive API docs are available at:

- Swagger UI: http://localhost:8000/api/v1/docs

## Configuration

Configuration is loaded from `.env` file or environment variables.
All settings and defaults are defined in `app/core/config.py`.

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/          # API route handlers
│   ├── core/                 # Configuration, logging, exceptions
│   ├── schemas/              # Pydantic request/response schemas
│   ├── dependencies/         # FastAPI dependency injection
│   ├── middleware/            # Custom middleware
│   ├── domain/               # Domain entities (future)
│   ├── application/          # Application services (future)
│   └── infrastructure/       # External adapters (future)
├── tests/                    # Test suite
└── pyproject.toml            # Project configuration