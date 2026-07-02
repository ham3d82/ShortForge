# ADR-0001: Clean Architecture with Domain-Driven Design

**Status**: Accepted  
**Date**: 2026-07-02  
**Author**: Principal Software Architect

---

## Decision

Adopt **Clean Architecture** (Robert C. Martin) layered with **Domain-Driven Design** tactical patterns for all backend development. The system is organized into five layers: Domain, Application, Infrastructure, API, and Worker/Media/AI. Dependencies point inward: the Domain layer has zero imports from any other layer.

---

## Context

ShortForge must orchestrate a pipeline: AI script generation, TTS, image generation, video composition, captioning, and YouTube publishing. Each stage involves different technologies (LLM APIs, FFmpeg, Whisper) that will change over time. The system must be:

1. **Testable**: Business logic must be testable without external dependencies.
2. **Replaceable**: AI providers, storage backends, and media engines must be swappable.
3. **Evolvable**: The pipeline will grow as new AI models and video formats emerge.
4. **Maintainable**: A solo developer using AI tooling must be able to work across layers.

---

## Rationale

1. **Dependency Inversion**: Domain entities (Project, Script, Video) define interfaces (ports). Infrastructure implements them. This means we can swap PostgreSQL for SQLite or S3 for local disk without touching business logic.

2. **Separation of Concerns**: 
   - API layer handles HTTP concerns (routing, middleware, serialization).
   - Application layer orchestrates use cases (GenerateScript, AssembleVideo).
   - Domain layer encapsulates business rules and state transitions.
   - Infrastructure layer implements persistence, external APIs, and queues.
   - AI/Media/Worker layers handle specialized processing.

3. **Testability**: Domain entities have zero dependencies, making unit tests trivial. Application use cases accept mocked ports.

4. **AI-Assisted Development**: Clean Architecture's clear boundaries allow AI coding tools to generate isolated components (a new provider adapter, a new use case) without risking regressions in unrelated layers.

---

## Consequences

### Positive
- High test coverage is achievable.
- Provider swapping requires only new adapter classes (no business logic changes).
- Framework lock-in is minimized (FastAPI could be replaced if needed).
- AI tools can generate isolated components safely.

### Negative
- Increased boilerplate: each layer needs its own models, DTOs, and mappers.
- Over-engineering risk for simple CRUD operations (mitigated by CQRS-lite: direct repository access for simple reads).

### Mitigation
- Use Pydantic models as both DTOs and domain objects where appropriate.
- Allow direct repository access for simple read-only queries.
- Document layer boundaries clearly.

---

## Compliance

- **Rule**: Domain models must not import `fastapi`, `sqlalchemy`, `httpx`, or any framework library.
- **Enforcement**: CI import linter (ruff with isort + custom rules).
- **Exception**: Pydantic `BaseModel` is permitted in domain definitions.