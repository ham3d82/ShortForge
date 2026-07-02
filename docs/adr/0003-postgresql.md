# ADR-0003: PostgreSQL as Primary Database

**Status**: Accepted  
**Date**: 2026-07-02  
**Author**: Principal Software Architect

---

## Decision

Use **PostgreSQL 16** as the primary database, accessed via **SQLAlchemy 2.0** (async) with **Alembic** for migrations. For local development and testing, support **SQLite** as a drop-in replacement via the same repository interfaces.

---

## Context

ShortForge needs to store projects, scripts, generated video metadata, user accounts, and job status. The database must support:

1. JSON/JSONB for flexible metadata and scene breakdowns.
2. Full-text search for script content (future).
3. Concurrent reads during video generation + writes from WebSocket status updates.
4. Easy local development without requiring a full PostgreSQL install.

---

## Rationale

1. **SQLAlchemy 2.0 Abstraction**: The repository pattern already abstracts the database implementation. By using SQLAlchemy's dialect system, we can use SQLite for local dev and testing, and PostgreSQL for production. The switch requires only a connection string change.

2. **JSONB Support**: Scene breakdowns, word timestamps, and generation metadata are inherently schema-flexible. PostgreSQL's JSONB with GIN indexes provides the right balance of structure and flexibility.

3. **Async Support**: SQLAlchemy 2.0's async engine (`AsyncSession`, `selectinload`) integrates cleanly with FastAPI's async request handling. No thread pool overhead for database operations.

4. **SQLite for Development**: SQLite requires zero setup, no Docker dependency, and enables instant schema iteration during development. The same Alembic migrations work for both databases with minor dialect adjustments.

---

## Consequences

### Positive
- Production-grade database with JSONB, full-text search, partitioning.
- SQLite for fast local development without Docker.
- Same repository code works for both databases.
- Alembic handles schema versioning cleanly.

### Negative
- Some PostgreSQL-specific features (partitioning, GIN indexes) require dialect-aware migrations.
- SQLite lacks concurrent writers (fine for single-developer, but requires PostgreSQL for multi-worker).
- JSONB queries differ slightly from SQLite JSON (mitigated by SQLAlchemy abstraction).

### Mitigation
- Isolate PostgreSQL-specific features behind the repository interface.
- Use SQLAlchemy's `with_variant()` for dialect-specific column types.
- Run integration tests against both SQLite and PostgreSQL in CI.

---

## Compliance

- **Rule**: All repository implementations must work with both SQLite and PostgreSQL.
- **Rule**: Migrations must be tested against both databases.
- **Enforcement**: CI matrix that runs tests against SQLite (fast) and PostgreSQL (Docker).