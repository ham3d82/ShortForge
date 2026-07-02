# ShortForge — Architectural Decision Log

> **Purpose**: Central record of every significant architectural decision made during development. Each entry captures the context, the decision, the rationale, and the consequences.

---

## How to Use

1. Each decision gets a unique ID (`D-001`, `D-002`, ...).
2. Formal Architecture Decision Records (ADRs) are in `docs/adr/` for major decisions.
3. This log includes both formal ADRs and smaller tactical decisions.
4. When revisiting a decision, update the Status and link to the new ADR that supersedes it.

---

## Decision Register

| ID | Title | Status | Date | Supersedes |
|----|-------|--------|------|------------|
| ADR-0001 | Clean Architecture with Domain-Driven Design | Accepted | 2026-07-02 | — |
| ADR-0002 | AI Provider Abstraction with Free/Open Defaults | Accepted | 2026-07-02 | — |
| ADR-0003 | PostgreSQL as Primary Database | Accepted | 2026-07-02 | — |
| ADR-0004 | FastAPI as Web Framework | Accepted | 2026-07-02 | — |
| ADR-0005 | Local-First Storage with Optional S3 | Accepted | 2026-07-02 | — |
| D-001 | SQLite as Development Database | Accepted | 2026-07-02 | — |
| D-002 | Celery for Async Task Queue | Accepted | 2026-07-02 | — |
| D-003 | FFmpeg via Subprocess for Video Processing | Accepted | 2026-07-02 | — |
| D-004 | Pydantic for DTO and Domain Models | Accepted | 2026-07-02 | — |
| D-005 | JWT with Short-Lived Access Tokens | Accepted | 2026-07-02 | — |
| D-006 | Cursor-Based Pagination | Accepted | 2026-07-02 | — |
| D-007 | Structured JSON Logging | Accepted | 2026-07-02 | — |
| D-008 | GPU Acceleration as Optional Plugin | Accepted | 2026-07-02 | — |
| D-009 | Pillow Fallback for Image Generation | Accepted | 2026-07-02 | — |
| D-010 | Multi-Language Deferred to Phase 2 | Accepted | 2026-07-02 | — |

---

## Decision Details

### D-001: SQLite as Development Database

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Developers need to run the application locally without installing PostgreSQL. Docker adds overhead for rapid iteration.

**Decision**: Use SQLite for local development via SQLAlchemy dialect switching. PostgreSQL is required for production and CI integration tests.

**Rationale**: SQLite requires zero setup, is file-based, and is fully supported by SQLAlchemy 2.0. The repository pattern abstracts database implementation, making the switch a connection string change.

**Consequences**:
- Fast local development without Docker dependency.
- Some PostgreSQL features (partitioning, GIN indexes) are unavailable in dev.
- Migrations must be tested against both databases.

---

### D-002: Celery for Async Task Queue

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Video generation is a long-running process (30 seconds to 5 minutes). The API must return immediately and report progress asynchronously.

**Decision**: Use Celery with Redis as the message broker for async task processing. Flower for monitoring.

**Rationale**: Celery is the most mature Python task queue. Redis is already used for caching and rate limiting. For MVP, tasks run in-process (Eager mode) can eliminate the Redis dependency entirely.

**Consequences**:
- MVP can use Celery Eager mode (no Redis required).
- Production uses Redis broker + Celery workers.
- Flower provides a web UI for monitoring.

---

### D-003: FFmpeg via Subprocess for Video Processing

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Video composition, encoding, caption burn-in, and thumbnail extraction all require FFmpeg.

**Decision**: Call FFmpeg via Python subprocess. No high-level Python wrapper (avoid MoviePy in production path).

**Rationale**: Direct subprocess gives full control over FFmpeg's filter graph, codec parameters, and GPU acceleration flags. MoviePy adds abstraction overhead and debugging complexity.

**Consequences**:
- Full access to FFmpeg features.
- CPU-only execution works with libx264.
- GPU acceleration (NVENC) is an optional flag (`-c:v h264_nvenc`).

---

### D-004: Pydantic for DTO and Domain Models

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: The system needs validated data transfer objects at the API boundary and domain models for business logic.

**Decision**: Use Pydantic V2 BaseModel for both DTOs and domain entities. Avoid creating separate domain models where Pydantic suffices.

**Rationale**: Pydantic V2 is fast, well-typed, and natively integrated with FastAPI. Using it for domain models avoids mapping overhead between layers for simple entities.

**Consequences**:
- Reduced boilerplate (no separate domain/DTO mapping).
- Domain models carry validation logic.
- Risk of coupling domain to Pydantic (acceptable trade-off for MVP).

---

### D-005: JWT with Short-Lived Access Tokens

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Users need authenticated access to the API. The system must support stateless authentication for horizontal scaling.

**Decision**: Use JWT access tokens (15-minute expiry) with opaque refresh tokens (7-day expiry) stored in the database.

**Rationale**: JWTs enable stateless auth for API workers. Short expiry limits damage from token leakage. Refresh tokens enable long-lived sessions without long-lived JWTs.

**Consequences**:
- Access tokens are stateless (no DB lookup on each request).
- Refresh tokens require DB storage (acceptable trade-off).
- WebSocket connections must handle token refresh.

---

### D-006: Cursor-Based Pagination

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Project listing, script versions, and publish history need pagination.

**Decision**: Use cursor-based pagination instead of offset-based. The cursor is an opaque Base64-encoded value.

**Rationale**: Cursor pagination is stable under concurrent writes (new records don't shift pages). It performs better on large datasets (no OFFSET). Opaque cursors prevent URL manipulation.

**Consequences**:
- Slightly more complex client implementation.
- No random page access (must paginate sequentially).
- Cursor encodes the last seen record's ID and sort value.

---

### D-007: Structured JSON Logging

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Debugging across API, workers, and media pipeline requires structured, searchable logs.

**Decision**: Use Python's `structlog` library for structured JSON logging with correlation IDs.

**Rationale**: JSON logs are parseable by log aggregation tools (Loki, ELK). Correlation IDs link requests across API → Celery → FFmpeg subprocess.

**Consequences**:
- All logs are structured JSON (no free-text parsing).
- Correlation ID is propagated via context variables.
- Development mode can use colored console output.

---

### D-008: GPU Acceleration as Optional Plugin

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: GPU acceleration dramatically speeds up video encoding and image generation, but must not be a requirement.

**Decision**: Make GPU acceleration completely optional. All GPU-dependent code paths must have CPU fallbacks. GPU detection happens at startup.

**Rationale**: The MVP must run on any developer machine without special hardware. GPU is a performance optimization, not a requirement.

**Consequences**:
- FFmpeg defaults to libx264 (CPU). NVENC is an opt-in.
- Image generation defaults to CPU-compatible models.
- Whisper can use CPU with `faster-whisper`.
- All GPU code is behind feature flags.

---

### D-009: Pillow Fallback for Image Generation

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Image generation via Stable Diffusion requires significant disk space and GPU. Not all development environments can run it.

**Decision**: Provide a Pillow-based fallback that generates simple but functional images (gradient backgrounds, text overlays, geometric shapes) when no AI image provider is available.

**Rationale**: Ensures the full pipeline can be tested without downloading 6GB+ of model files. The visual result is basic, but the pipeline logic is validated.

**Consequences**:
- Full pipeline works without any ML model downloads.
- Pillow images are visually simple but functionally adequate.
- Users see a clear quality difference when they enable AI generation.

---

### D-010: Multi-Language Deferred to Phase 2

**Status**: Accepted  
**Date**: 2026-07-02

**Context**: Multi-language support adds significant complexity (translation pipeline, per-language TTS, subtitle alignment, cultural adaptation).

**Decision**: Defer multi-language support to Phase 2. MVP supports English only.

**Rationale**: The MVP goal is to generate a complete Shorts video from one idea. Adding 10+ languages multiplies testing, provider configuration, and quality evaluation scope without adding core pipeline value.

**Consequences**:
- MVP scope is reduced by ~20%.
- Architecture supports adding languages later via provider abstraction.
- Script generation prompts are English-only initially.
- TTS defaults to English voices.
- Whisper is configured for English transcription.