# ADR-0005: Local-First Storage with Optional S3

**Status**: Accepted  
**Date**: 2026-07-02  
**Author**: Principal Software Architect

---

## Decision

Use **local filesystem storage** as the default for all media files (generated images, audio, videos, thumbnails). Support **S3-compatible storage** (MinIO for development, AWS S3 for production) as an optional upgrade via the same storage adapter interface.

---

## Context

ShortForge generates and stores media assets at every pipeline stage:

- Generated images (PNG, 5-10MB each)
- TTS audio files (MP3, 1-5MB each)
- Rendered videos (MP4, 15-150MB each)
- Thumbnails (JPEG, 200KB each)
- Caption files (SRT/ASS, <100KB each)

The storage solution must:

1. Work without any cloud infrastructure for MVP development.
2. Support easy file access for debugging and inspection.
3. Allow future migration to cloud storage without application changes.
4. Handle files up to 256MB (YouTube's upload limit).

---

## Rationale

1. **MVP Simplicity**: Local storage requires zero configuration, zero cloud accounts, and zero network dependencies. The developer creates files in a local directory and inspects them with any file manager.

2. **Storage Adapter Pattern**: The `IStorageProvider` interface abstracts all file operations (save, read, delete, list). Switching from local to S3 requires only a new adapter class and a config change. No business logic changes.

3. **Debugging Velocity**: During development, being able to open `./media/output/video_001.mp4` directly in a media player is significantly faster than downloading from S3. This accelerates the iteration cycle for a solo developer.

4. **Path to Production**: When the application is deployed, the same codebase connects to S3/MinIO. The local adapter becomes a development-only dependency.

---

## Consequences

### Positive
- Zero infrastructure required for MVP development.
- Instant file access for debugging.
- Simple backup (copy the media directory).
- No cloud costs during development.

### Negative
- Local storage doesn't scale horizontally (fine for MVP, needs S3 for production).
- File system may fill up with generated media (mitigated by cleanup tasks).
- Not suitable for multi-server deployments without shared NFS (use S3 instead).

### Mitigation
- Implement cleanup tasks (Celery Beat) to remove files older than 30 days.
- The storage adapter interface makes S3 migration a configuration change.
- Document the migration path clearly.

---

## Compliance

- **Rule**: All file operations must go through `IStorageProvider` interface.
- **Rule**: No direct filesystem access in business logic or API layers.
- **Enforcement**: Architecture tests that verify only infrastructure layer imports `os`, `shutil`, or `boto3`.