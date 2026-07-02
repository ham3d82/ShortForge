# ShortForge — Technical Debt Register

> **Purpose**: Track every intentional shortcut, temporary workaround, and known limitation. Each item is a conscious trade-off made to ship the MVP faster. Debt items are prioritized and scheduled for resolution.

---

## How to Use

1. Each debt item gets a unique ID (`TD-001`, `TD-002`, ...).
2. **Priority**: P0 = Must fix before production, P1 = Should fix in Phase 2, P2 = Nice to have.
3. When a debt item is resolved, move it to the "Resolved" section with the resolution date.
4. Before adding new debt, check if a tracked item already covers it.

---

## Active Debt Items

### TD-001: Pydantic Models as Domain Entities

| Field | Value |
|-------|-------|
| **Description** | Domain entities inherit from Pydantic BaseModel instead of being pure Python objects. This couples the domain layer to Pydantic. |
| **Reason** | Avoids creating separate domain models + DTOs + ORM models (3 representations). Pydantic V2 is fast and well-typed. For MVP, the reduced boilerplate is worth the coupling. |
| **Planned Resolution** | Extract pure domain interfaces when/if Pydantic becomes a bottleneck. Create domain-specific base classes that don't inherit from BaseModel. |
| **Priority** | P2 |
| **Effort Estimate** | 2-3 days |
| **Trigger** | If we need to swap Pydantic for another validation library, or if Pydantic's serialization overhead becomes measurable. |

---

### TD-002: Celery Eager Mode for MVP

| Field | Value |
|-------|-------|
| **Description** | MVP uses Celery's Eager mode (`task_always_eager=True`), which runs tasks synchronously in-process. No Redis or worker process is required. |
| **Reason** | Eliminates Redis dependency for MVP development. A solo developer doesn't need a message broker to test the pipeline. |
| **Planned Resolution** | Switch to async Celery with Redis broker when deploying to production or when multiple workers are needed. |
| **Priority** | P1 |
| **Effort Estimate** | 1 day |
| **Trigger** | First production deployment or when pipeline latency becomes an issue. |

---

### TD-003: No Authentication for MVP

| Field | Value |
|-------|-------|
| **Description** | MVP may skip user authentication entirely or use a single hardcoded API key. No JWT, no user registration, no role-based access. |
| **Reason** | Authentication adds significant scope (registration, login, token refresh, password reset, OAuth2). For MVP, the focus is on the generation pipeline. |
| **Planned Resolution** | Implement JWT auth with user registration before any multi-user deployment. |
| **Priority** | P0 |
| **Effort Estimate** | 3-4 days |
| **Trigger** | Before any deployment where multiple users can access the system. |

---

### TD-004: No Rate Limiting

| Field | Value |
|-------|-------|
| **Description** | MVP has no rate limiting on API endpoints. A user could trigger unlimited generation requests. |
| **Reason** | Rate limiting adds middleware complexity. For a solo developer testing locally, it's unnecessary overhead. |
| **Planned Resolution** | Implement Redis-based rate limiting before any production deployment. |
| **Priority** | P1 |
| **Effort Estimate** | 1 day |
| **Trigger** | Production deployment or when testing reveals resource exhaustion. |

---

### TD-005: No WebSocket for Progress Updates

| Field | Value |
|-------|-------|
| **Description** | MVP uses polling (`GET /jobs/{id}`) instead of WebSocket for generation progress. |
| **Reason** | WebSocket adds connection management complexity. Polling is simpler to implement and debug. For a solo developer, polling at 2-second intervals is acceptable. |
| **Planned Resolution** | Implement WebSocket endpoint for real-time progress when the frontend is built and polling latency becomes noticeable. |
| **Priority** | P1 |
| **Effort Estimate** | 2 days |
| **Trigger** | Frontend development begins or when polling overhead becomes measurable. |

---

### TD-006: No Background Music Mixing

| Field | Value |
|-------|-------|
| **Description** | MVP generates voiceover-only audio. Background music mixing (ducking, crossfade) is not implemented. |
| **Reason** | Audio mixing adds significant complexity (BGM selection, volume ducking, licensing). Voiceover-only is functional for MVP. |
| **Planned Resolution** | Implement audio mixing with configurable BGM in Phase 2. |
| **Priority** | P2 |
| **Effort Estimate** | 2-3 days |
| **Trigger** | User feedback requesting background music. |

---

### TD-007: No Image Upscaling

| Field | Value |
|-------|-------|
| **Description** | MVP generates images at output resolution directly. No Real-ESRGAN upscaling pass. |
| **Reason** | Upscaling requires downloading a ~100MB model file and adds GPU-dependent processing time. Direct generation at 1080x1920 is acceptable for MVP. |
| **Planned Resolution** | Add optional upscaling pass when GPU is available and quality requirements increase. |
| **Priority** | P2 |
| **Effort Estimate** | 2 days |
| **Trigger** | When image quality feedback indicates upscaling would help. |

---

### TD-008: No Image Animation (Ken Burns / Deforum)

| Field | Value |
|-------|-------|
| **Description** | MVP uses static images as video backgrounds. No Ken Burns effect or Deforum animation. |
| **Reason** | Animation adds FFmpeg filter complexity and GPU dependency. Static images produce a functional video. |
| **Planned Resolution** | Implement Ken Burns effect (FFmpeg zoompan) in Phase 2. Deforum animation remains Phase 3. |
| **Priority** | P2 |
| **Effort Estimate** | Ken Burns: 1 day. Deforum: 3-4 days. |
| **Trigger** | When static images feel too static for the target audience. |

---

### TD-009: No Scene Transitions

| Field | Value |
|-------|-------|
| **Description** | MVP uses hard cuts between scenes. No fade, crossfade, or slide transitions. |
| **Reason** | Transitions add FFmpeg filter graph complexity. Hard cuts are functional and common in Shorts content. |
| **Planned Resolution** | Add configurable transition effects (fade, crossfade, slide) in Phase 2. |
| **Priority** | P2 |
| **Effort Estimate** | 1-2 days |
| **Trigger** | When hard cuts feel jarring in longer videos (>60s). |

---

### TD-010: No Thumbnail Generation

| Field | Value |
|-------|-------|
| **Description** | MVP does not generate video thumbnails. The first frame of the video is used as a default. |
| **Reason** | Thumbnail generation (frame extraction + text overlay) is a separate pipeline step. Not required for core video generation. |
| **Planned Resolution** | Implement thumbnail generation (frame extraction + AI enhancement + text overlay) in Phase 2. |
| **Priority** | P2 |
| **Effort Estimate** | 1-2 days |
| **Trigger** | Before YouTube publishing feature is built. |

---

### TD-011: No YouTube Publishing

| Field | Value |
|-------|-------|
| **Description** | MVP generates videos to local disk only. No YouTube API integration for upload or publishing. |
| **Reason** | YouTube API integration requires OAuth2 setup, quota management, and resumable upload handling. The core pipeline (script → video) is the MVP focus. |
| **Planned Resolution** | Implement YouTube publishing in Phase 2 after the core pipeline is stable. |
| **Priority** | P1 |
| **Effort Estimate** | 5-7 days |
| **Trigger** | When the generation pipeline is stable and producing quality videos. |

---

### TD-012: No Prompt Versioning

| Field | Value |
|-------|-------|
| **Description** | MVP uses hardcoded prompt templates. No versioning, no A/B testing, no prompt registry. |
| **Reason** | Prompt versioning adds infrastructure (database storage, version comparison, A/B test framework). For MVP, iterating on prompts by editing text files is faster. |
| **Planned Resolution** | Implement PromptRegistry with versioning and A/B testing in Phase 2. |
| **Priority** | P2 |
| **Effort Estimate** | 3-4 days |
| **Trigger** | When prompt iteration becomes frequent enough that version tracking is needed. |

---

### TD-013: No Quality Evaluation

| Field | Value |
|-------|-------|
| **Description** | MVP does not evaluate script or video quality. Generated content is accepted as-is. |
| **Reason** | Quality evaluation requires a separate LLM call or heuristic analysis. For MVP, the developer reviews output manually. |
| **Planned Resolution** | Implement script quality scoring (LLM-based) and basic video quality checks (resolution, duration, bitrate) in Phase 2. |
| **Priority** | P2 |
| **Effort Estimate** | 3-5 days |
| **Trigger** | When manual review becomes a bottleneck or when users report inconsistent quality. |

---

### TD-014: No Content Safety Filter

| Field | Value |
|-------|-------|
| **Description** | MVP does not filter generated content for policy violations (NSFW, hate speech, etc.). |
| **Reason** | Content filtering adds complexity and is not needed for a solo developer testing their own prompts. |
| **Planned Resolution** | Implement multi-layer content safety filter (input + output + image) before any public deployment. |
| **Priority** | P0 |
| **Effort Estimate** | 2-3 days |
| **Trigger** | Before any deployment where external users can generate content. |

---

### TD-015: No Audit Log

| Field | Value |
|-------|-------|
| **Description** | MVP does not track changes to projects, scripts, or videos. No immutable audit trail. |
| **Reason** | Audit logging adds a write-heavy table and partitioning complexity. Not needed for single-developer use. |
| **Planned Resolution** | Implement audit_log table with monthly partitioning before production deployment. |
| **Priority** | P1 |
| **Effort Estimate** | 2-3 days |
| **Trigger** | Production deployment or when debugging requires understanding what changed. |

---

### TD-016: No Soft Deletes

| Field | Value |
|-------|-------|
| **Description** | MVP uses hard deletes (DELETE FROM ...) instead of soft deletes (deleted_at timestamp). |
| **Reason** | Soft deletes add query complexity (every SELECT needs `WHERE deleted_at IS NULL`). For MVP, hard deletes are simpler. |
| **Planned Resolution** | Add `deleted_at` columns and update all queries to filter soft-deleted records. |
| **Priority** | P2 |
| **Effort Estimate** | 1-2 days |
| **Trigger** | When accidental data loss becomes a concern. |

---

### TD-017: No Database Migrations for Schema Changes

| Field | Value |
|-------|-------|
| **Description** | MVP may use SQLAlchemy's `create_all()` for initial schema and manual ALTER TABLE for changes. No Alembic migration chain. |
| **Reason** | Alembic migration management adds process overhead. For rapid schema iteration during MVP, direct schema changes are faster. |
| **Planned Resolution** | Set up Alembic with proper migration chain before any production deployment or when collaborating with other developers. |
| **Priority** | P1 |
| **Effort Estimate** | 1 day |
| **Trigger** | Production deployment or when schema changes need to be shared. |

---

### TD-018: No Caching

| Field | Value |
|-------|-------|
| **Description** | MVP has no caching layer. Every request hits the database or AI provider. |
| **Reason** | Caching adds Redis dependency and cache invalidation complexity. For a solo developer, uncached performance is acceptable. |
| **Planned Resolution** | Implement Redis caching for AI responses (prompt caching) and database query results before production deployment. |
| **Priority** | P1 |
| **Effort Estimate** | 2-3 days |
| **Trigger** | When AI API costs become significant or when database query latency is noticeable. |

---

### TD-019: No Monitoring or Metrics

| Field | Value |
|-------|-------|
| **Description** | MVP has no Prometheus metrics, no Grafana dashboards, no Sentry error tracking. |
| **Reason** | Monitoring infrastructure adds significant setup time. For a solo developer, console logs and manual inspection are sufficient. |
| **Planned Resolution** | Set up Prometheus + Grafana for API metrics, Sentry for error tracking before production deployment. |
| **Priority** | P1 |
| **Effort Estimate** | 3-4 days |
| **Trigger** | Production deployment or when debugging requires historical metrics. |

---

### TD-020: No CI/CD Pipeline

| Field | Value |
|-------|-------|
| **Description** | MVP has no automated CI/CD. Code is tested and deployed manually. |
| **Reason** | CI/CD setup (GitHub Actions, Docker build, test runner) adds overhead before there's a codebase to test. |
| **Planned Resolution** | Set up GitHub Actions with lint, test, and build stages when the first feature is complete. |
| **Priority** | P1 |
| **Effort Estimate** | 1-2 days |
| **Trigger** | When the first feature branch is ready for merging. |

---

## Resolved Debt Items

*None yet. This section will grow as debt items are paid down.*

---

## Debt Summary

| Priority | Count | Total Est. Effort |
|----------|-------|-------------------|
| P0 (Must fix) | 2 | 5-7 days |
| P1 (Should fix) | 9 | 19-27 days |
| P2 (Nice to have) | 9 | 16-25 days |
| **Total** | **20** | **40-59 days** |

### Debt Burndown Target

- **Before Production**: Resolve all P0 items (TD-003, TD-014).
- **Phase 2**: Resolve P1 items (TD-002, TD-004, TD-005, TD-011, TD-015, TD-017, TD-018, TD-019, TD-020).
- **Phase 3+**: Resolve P2 items as time permits.