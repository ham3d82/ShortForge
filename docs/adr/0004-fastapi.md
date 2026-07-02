# ADR-0004: FastAPI as Web Framework

**Status**: Accepted  
**Date**: 2026-07-02  
**Author**: Principal Software Architect

---

## Decision

Use **FastAPI** as the web framework for the backend API. The application is served via **Uvicorn** with ASGI. All request/response validation uses **Pydantic V2** schemas.

---

## Context

The backend must expose a RESTful API for the frontend and support:

1. Async request handling for long-polling and concurrent connections.
2. Automatic API documentation (OpenAPI/Swagger) for developer experience.
3. Strong input validation to prevent malformed data from reaching the pipeline.
4. WebSocket support for real-time generation progress updates.
5. Dependency injection for clean separation of concerns.

---

## Rationale

1. **Native Async**: FastAPI is built on Starlette and supports async natively. This is critical for the generation pipeline where we need to:
   - Accept a generation request and return immediately (202 Accepted).
   - Poll job status without blocking.
   - Stream progress via WebSocket.

2. **Pydantic Integration**: FastAPI uses Pydantic V2 for request/response validation. Since we already use Pydantic for domain DTOs, this eliminates redundant validation layers.

3. **Auto-Generated Docs**: OpenAPI documentation is generated automatically from type annotations. This reduces documentation maintenance and provides a testable API surface.

4. **Dependency Injection**: FastAPI's `Depends()` system maps cleanly to Clean Architecture's dependency injection needs. We can inject repository implementations, service instances, and configuration without a separate DI container.

5. **Lightweight**: FastAPI has minimal overhead compared to Django. For a solo developer, faster iteration and simpler debugging are significant advantages.

---

## Consequences

### Positive
- Automatic OpenAPI docs with zero configuration.
- Pydantic validation at the boundary prevents invalid data from entering the domain.
- Async request handling without thread pool management.
- WebSocket support built-in (no separate library needed).

### Negative
- Smaller ecosystem than Django (no built-in admin, ORM, or auth).
- ASGI deployment requires Uvicorn or Gunicorn with Uvicorn workers (slightly more complex than WSGI).
- Less community content for niche use cases.

### Mitigation
- FastAPI's ecosystem is mature enough for our needs (auth via python-jose, DB via SQLAlchemy).
- Docker handles ASGI deployment complexity.
- Community is large and active (60k+ GitHub stars).

---

## Compliance

- **Rule**: All route handlers must use Pydantic models for request/response typing.
- **Rule**: Business logic must not live in route handlers (delegate to use cases).
- **Enforcement**: Code review and architecture tests that verify route handler structure.