# ShortForge — API Specification

> **Author**: Principal Software Architect  
> **Version**: 1.0.0  
> **Last Updated**: 2026-07-02

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [API Conventions](#2-api-conventions)
3. [Authentication](#3-authentication)
4. [Endpoints Overview](#4-endpoints-overview)
5. [Detailed Endpoint Specifications](#5-detailed-endpoint-specifications)
6. [WebSocket Events](#6-websocket-events)
7. [Error Handling](#7-error-handling)
8. [Rate Limiting](#8-rate-limiting)
9. [API Versioning](#9-api-versioning)

---

## 1. Design Principles

| Principle | Application |
|-----------|-------------|
| **RESTful** | Resource-based URLs, standard HTTP methods |
| **Consistent Naming** | `snake_case` for fields, kebab-case for endpoints |
| **Idempotent Mutations** | PUT/PATCH for updates, idempotency-key header for creates |
| **Pagination** | Cursor-based for lists, with `next_cursor` in responses |
| **Async Operations** | 202 Accepted + polling via status endpoint |
| **Self-Describing** | HATEOAS-style links in responses for discoverability |
| **Pydantic Validation** | All request/response schemas validated at compile time |
| **Backward Compatible** | Fields are additive only; deprecation notices via headers |

---

## 2. API Conventions

### 2.1 Base URL

```
Development:  http://localhost:8000/api/v1
Production:   https://api.shortforge.com/api/v1
```

### 2.2 Standard Headers

| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes (auth routes) | `Bearer <access_token>` |
| `X-Idempotency-Key` | No | UUID for idempotent creates |
| `X-Request-ID` | Recommended | UUID for request tracing |
| `Accept-Language` | No | Locale for error messages |
| `Content-Type` | Yes | `application/json` |

### 2.3 Response Envelope

```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-07-02T04:00:00Z",
    "version": "1.0"
  }
}
```

### 2.4 Paginated Response

```json
{
  "data": [ ... ],
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-07-02T04:00:00Z",
    "version": "1.0",
    "pagination": {
      "cursor": "eyJpZCI6IjEyMyJ9",
      "next_cursor": "eyJpZCI6IjI0NSJ9",
      "has_more": true,
      "limit": 20
    }
  }
}
```

### 2.5 Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid field value",
    "details": [
      {
        "field": "target_duration",
        "message": "Must be between 15 and 180 seconds",
        "code": "INVALID_DURATION"
      }
    ],
    "request_id": "req_abc123"
  }
}
```

---

## 3. Authentication

### 3.1 Token Flow

```
┌──────────┐    ┌─────────────────────┐    ┌──────────────────────┐
│  Client  │    │  POST /auth/login   │    │  JWT Tokens Issued   │
│          │───▶│  {email, password}  │───▶│  access_token (15m)  │
│          │    │                     │    │  refresh_token (7d)  │
│          │    └─────────────────────┘    └──────────────────────┘
│          │                                        │
│          │    ┌─────────────────────┐            │
│          │    │  POST /auth/refresh │◄───────────┘
│          │───▶│  {refresh_token}    │            │
│          │    └─────────────────────┘            │
│          │                                        ▼
│          │    ┌─────────────────────┐    ┌──────────────────────┐
│          │    │  POST /auth/logout  │    │  Token Blacklisted   │
│          └───▶│  {refresh_token}    │───▶│  Session Cleared     │
│               └─────────────────────┘    └──────────────────────┘
```

### 3.2 OAuth2 (YouTube)

```
┌──────────┐    ┌─────────────────────────────┐    ┌──────────────┐
│  Client  │    │  GET /auth/youtube/authorize │    │  Google OAuth │
│          │───▶│  redirect to Google          │───▶│  Consent Page │
│          │    └─────────────────────────────┘    └──────────────┘
│          │                                              │
│          │    ┌─────────────────────────────┐           │
│          │    │  GET /auth/youtube/callback  │◄──────────┘
│          │───▶│  ?code=xxx&state=yyy        │
│          │    └─────────────────────────────┘
│          │              │
│          │              ▼
│          │    ┌─────────────────────────────┐
│          │    │  Tokens stored in DB         │
│          └───▶│  Redirect to frontend        │
│               └─────────────────────────────┘
```

---

## 4. Endpoints Overview

### 4.1 Auth Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/auth/register` | Create new user account | No |
| POST | `/auth/login` | Authenticate and get tokens | No |
| POST | `/auth/refresh` | Refresh access token | Refresh |
| POST | `/auth/logout` | Invalidate refresh token | Yes |
| GET | `/auth/me` | Get current user profile | Yes |
| PATCH | `/auth/me` | Update current user profile | Yes |
| GET | `/auth/youtube/authorize` | Start YouTube OAuth2 flow | Yes |
| GET | `/auth/youtube/callback` | Handle OAuth2 callback | No |

### 4.2 Project Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects` | Create new project | Yes |
| GET | `/projects` | List user's projects | Yes |
| GET | `/projects/{id}` | Get project details | Yes |
| PATCH | `/projects/{id}` | Update project | Yes |
| DELETE | `/projects/{id}` | Archive/delete project | Yes |
| POST | `/projects/{id}/duplicate` | Duplicate project | Yes |

### 4.3 Script Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects/{id}/scripts` | Generate script | Yes |
| GET | `/projects/{id}/scripts` | List script versions | Yes |
| GET | `/projects/{id}/scripts/{script_id}` | Get script content | Yes |
| PATCH | `/projects/{id}/scripts/{script_id}` | Edit script manually | Yes |
| POST | `/projects/{id}/scripts/{script_id}/approve` | Approve script | Yes |
| POST | `/projects/{id}/scripts/{script_id}/reject` | Reject script | Yes |
| POST | `/projects/{id}/scripts/{script_id}/regenerate` | Regenerate with feedback | Yes |

### 4.4 Audio Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects/{id}/audio` | Generate TTS audio | Yes |
| GET | `/projects/{id}/audio` | Get audio generation status | Yes |
| GET | `/projects/{id}/audio/{voiceover_id}` | Get voiceover details | Yes |
| DELETE | `/projects/{id}/audio/{voiceover_id}` | Delete voiceover | Yes |
| GET | `/projects/{id}/audio/{voiceover_id}/stream` | Stream audio file | Yes |

### 4.5 Image Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects/{id}/images` | Generate images | Yes |
| GET | `/projects/{id}/images` | List project images | Yes |
| GET | `/projects/{id}/images/{image_id}` | Get image details | Yes |
| POST | `/projects/{id}/images/{image_id}/upscale` | Upscale image | Yes |
| POST | `/projects/{id}/images/{image_id}/animate` | Animate image | Yes |
| DELETE | `/projects/{id}/images/{image_id}` | Delete image | Yes |

### 4.6 Caption Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects/{id}/captions` | Generate captions | Yes |
| GET | `/projects/{id}/captions` | Get captions | Yes |
| PUT | `/projects/{id}/captions` | Update captions manually | Yes |
| POST | `/projects/{id}/captions/translate` | Translate captions | Yes |

### 4.7 Video Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects/{id}/videos` | Start video generation | Yes |
| GET | `/projects/{id}/videos` | List video versions | Yes |
| GET | `/projects/{id}/videos/{video_id}` | Get video details | Yes |
| GET | `/projects/{id}/videos/{video_id}/preview` | Get streaming URL | Yes |
| POST | `/projects/{id}/videos/{video_id}/thumbnail` | Generate thumbnail | Yes |

### 4.8 Publishing Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects/{id}/publish` | Publish to YouTube | Yes |
| GET | `/projects/{id}/publishes` | List publish history | Yes |
| GET | `/projects/{id}/publishes/{publish_id}` | Get publish status | Yes |
| POST | `/projects/{id}/publishes/{publish_id}/retry` | Retry failed publish | Yes |
| DELETE | `/projects/{id}/publishes/{publish_id}` | Cancel scheduled publish | Yes |

### 4.9 Job / Status Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/projects/{id}/jobs` | List generation jobs | Yes |
| GET | `/jobs/{job_id}` | Get job status | Yes |
| GET | `/projects/{id}/status` | Get full pipeline status | Yes |

### 4.10 YouTube Account Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/accounts/youtube` | List connected accounts | Yes |
| GET | `/accounts/youtube/{account_id}` | Get account details | Yes |
| DELETE | `/accounts/youtube/{account_id}` | Disconnect account | Yes |

### 4.11 Admin Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/admin/users` | List all users | Admin |
| GET | `/admin/users/{id}` | Get user details | Admin |
| PATCH | `/admin/users/{id}` | Update user (suspend/role) | Admin |
| GET | `/admin/stats` | System statistics | Admin |
| GET | `/admin/workers` | Worker status | Admin |
| GET | `/admin/queue` | Queue depth per type | Admin |

### 4.12 Media/Upload Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | `/projects/{id}/media/upload` | Upload media file | Yes |
| GET | `/projects/{id}/media` | List uploaded media | Yes |
| DELETE | `/projects/{id}/media/{media_id}` | Delete media | Yes |

---

## 5. Detailed Endpoint Specifications

### 5.1 Authentication

#### POST `/auth/register`

```yaml
summary: Register a new user account
request:
  body:
    email: string (required, valid email)
    password: string (required, min 8 chars, 1 upper, 1 number)
    display_name: string (required, 2-100 chars)
    accept_terms: boolean (required, must be true)
response:
  201:
    user_id: uuid
    email: string
    display_name: string
    role: string
    created_at: datetime
  409: Email already registered
  422: Validation error
```

#### POST `/auth/login`

```yaml
summary: Authenticate and receive JWT tokens
request:
  body:
    email: string (required)
    password: string (required)
response:
  200:
    access_token: string (JWT, 15 min expiry)
    refresh_token: string (opaque, 7 day expiry)
    token_type: "bearer"
    expires_in: 900
    user:
      user_id: uuid
      email: string
      display_name: string
      role: string
  401: Invalid credentials
```

### 5.2 Projects

#### POST `/projects`

```yaml
summary: Create a new video project
request:
  body:
    topic: string (required, 10-500 chars)
    tone: enum (educational, humorous, inspirational, entertaining, dramatic, controversial)
    target_duration: int (15-180, default 30)
    language: string (ISO 639-1, default "en")
    title: string (optional, 3-100 chars)
    tags: string[] (optional, max 10)
    keywords: string[] (optional, max 20)
    background_media: object (optional)
      type: enum (video, image, none)
      source: string (URL or media_id)
    style_preset: string (optional, default "modern")
response:
  201:
    project: ProjectObject
    links:
      self: /api/v1/projects/{id}
      scripts: /api/v1/projects/{id}/scripts
```

#### GET `/projects`

```yaml
summary: List user's projects with pagination
query_params:
  status: enum (optional, filter by status)
  sort: enum (created_at, updated_at, title; default created_at)
  order: enum (asc, desc; default desc)
  limit: int (1-100, default 20)
  cursor: string (optional, from previous response)
response:
  200:
    data: ProjectObject[]
    meta.pagination:
      cursor: string
      next_cursor: string | null
      has_more: boolean
      limit: int
```

#### GET `/projects/{id}`

```yaml
summary: Get full project details including pipeline status
response:
  200:
    project: ProjectObject (full)
    pipeline_status:
      script: JobStatus
      audio: JobStatus
      image: JobStatus
      caption: JobStatus
      video: JobStatus
      thumbnail: JobStatus
    latest_script: ScriptObject | null
    latest_video: VideoObject | null
  404: Project not found
```

### 5.3 Scripts

#### POST `/projects/{id}/scripts`

```yaml
summary: Generate a new script (async, returns immediately)
request:
  body:
    hooks_count: int (1-5, optional, default 3)
    include_statistics: boolean (optional, default false)
    creativity: float (0.0-1.0, optional, default 0.7)
    reference_links: string[] (optional, max 3)
response:
  202:
    job_id: uuid
    status: "generating"
    estimated_time_seconds: int
    links:
      status: /api/v1/jobs/{job_id}
```

#### PATCH `/projects/{id}/scripts/{script_id}`

```yaml
summary: Manually edit a script (creates new version)
request:
  body:
    hook_text: string (optional)
    body_text: string (optional)
    cta_text: string (optional)
    scene_breakdown: SceneBreakdown[] (optional, full replacement)
response:
  200:
    script: ScriptObject (new version)
    version: int (incremented)
```

### 5.4 Videos

#### POST `/projects/{id}/videos`

```yaml
summary: Start full video generation pipeline
request:
  body:
    script_id: uuid (optional, uses latest approved if omitted)
    voiceover_id: uuid (optional, generates new if omitted)
    caption_style: CaptionStyleConfig (optional)
    background_music: object (optional)
      source: enum (none, ai_generated, uploaded)
      media_id: uuid (if uploaded)
      volume: float (0.0-1.0, default 0.3)
    output_format: enum (mp4, webm; default mp4)
    quality: enum (draft, standard, high; default standard)
      draft: 480p, lower bitrate, faster render
      standard: 1080p, balanced
      high: 1080p, high bitrate, slowest
response:
  202:
    job_id: uuid
    estimated_time_seconds: int
    links:
      status: /api/v1/jobs/{job_id}
      preview: /api/v1/projects/{id}/videos/{video_id}/preview
```

### 5.5 Publishing

#### POST `/projects/{id}/publish`

```yaml
summary: Schedule a video for publishing to YouTube
request:
  body:
    video_id: uuid (required)
    account_id: uuid (required, which YouTube account)
    title: string (required, 3-100 chars)
    description: string (optional, max 5000 chars)
    tags: string[] (optional, max 30)
    category_id: string (optional, YouTube category)
    visibility: enum (public, unlisted, private; default unlisted)
    schedule_at: datetime (optional, if scheduling future)
    notify_subscribers: boolean (default true)
response:
  202:
    publish_id: uuid
    status: "pending" | "scheduled"
    scheduled_for: datetime | null
    links:
      status: /api/v1/projects/{id}/publishes/{publish_id}
```

### 5.6 Jobs

#### GET `/jobs/{job_id}`

```yaml
summary: Poll job status (used for async operations)
response:
  200:
    job_id: uuid
    job_type: string
    status: enum (pending, running, completed, failed, retrying)
    progress_pct: int (0-100)
    started_at: datetime | null
    completed_at: datetime | null
    error_message: string | null
    result: object | null (present when completed)
      script_id: uuid (if job_type=script)
      video_id: uuid (if job_type=video)
      voiceover_id: uuid (if job_type=audio)
      image_ids: uuid[] (if job_type=image)
```

---

## 6. WebSocket Events

### 6.1 Connection

```
WS /api/v1/ws?token={access_token}
```

### 6.2 Event Types

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `job.updated` | Server → Client | `{ job_id, status, progress_pct }` | Job progress update |
| `pipeline.completed` | Server → Client | `{ project_id, video_id }` | Full pipeline done |
| `pipeline.failed` | Server → Client | `{ project_id, job_id, error }` | Pipeline failure |
| `script.ready` | Server → Client | `{ project_id, script_id }` | Script generation completed |
| `progress` | Server → Client | `{ project_id, step, pct }` | Generic progress |

### 6.3 Client Subscribe

```json
// Client sends subscribe message
{
  "type": "subscribe",
  "channels": ["project:{project_id}", "user:{user_id}"]
}
```

---

## 7. Error Handling

### 7.1 Error Codes

| HTTP Status | Error Code | Description |
|-------------|-----------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid request body/params |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 401 | `TOKEN_EXPIRED` | Access token expired |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 404 | `NOT_FOUND` | Resource doesn't exist |
| 409 | `CONFLICT` | Resource already exists / conflict |
| 409 | `SCRIPT_NOT_APPROVED` | Cannot generate video without approved script |
| 422 | `UNPROCESSABLE_ENTITY` | Semantic validation failure |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Unexpected server error |
| 502 | `UPSTREAM_ERROR` | External service failure |
| 503 | `SERVICE_UNAVAILABLE` | System overload / maintenance |

### 7.2 Retry-After Header

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1688888888
```

### 7.3 Idempotency

```http
POST /api/v1/projects/{id}/scripts
X-Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000

# If the same key is reused within 24h:
HTTP/1.1 200 OK  # Returns previously created resource
X-Idempotency-Replayed: true
```

---

## 8. Rate Limiting

### 8.1 Limits by Tier

| Tier | Requests/min | Burst | Concurrent Jobs |
|------|-------------|-------|-----------------|
| **Creator** (free) | 60 | 10 | 3 |
| **Premium** | 300 | 50 | 20 |
| **Admin** | 1000 | 200 | 100 |

### 8.2 Endpoint-Specific Limits

| Endpoint | Limit | Scope |
|----------|-------|-------|
| `POST /scripts` | 10/min | Per project |
| `POST /videos` | 5/min | Per user |
| `POST /images` | 20/min | Per user |
| `POST /publish` | 10/min | Per user |
| `POST /auth/login` | 5/min | Per IP |

---

## 9. API Versioning

### 9.1 Strategy

- **URL versioning**: `/api/v1/`, `/api/v2/`
- **Header deprecation**: `Sunset: Sat, 01 Jan 2027 00:00:00 GMT`
- **Migration window**: 6 months between major version releases
- **Backward compatibility**: New fields are additive only; breaking changes require new version

### 9.2 Deprecation Headers

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 01 Jan 2027 00:00:00 GMT
Link: </api/v2/projects>; rel="successor-version"
```

---

## Appendix: Common Object Schemas

### ProjectObject

```json
{
  "project_id": "uuid",
  "user_id": "uuid",
  "title": "string | null",
  "topic": "string",
  "tone": "enum",
  "target_duration": 30,
  "language": "en",
  "status": "draft",
  "generation_progress": {
    "script": "pending",
    "audio": "pending",
    "image": "pending",
    "caption": "pending",
    "video": "pending",
    "thumbnail": "pending"
  },
  "tags": ["tech", "tutorial"],
  "keywords": ["python", "ai"],
  "created_at": "2026-07-02T04:00:00Z",
  "updated_at": "2026-07-02T04:00:00Z"
}
```

### ScriptObject

```json
{
  "script_id": "uuid",
  "project_id": "uuid",
  "version": 1,
  "status": "ready",
  "hook_text": "string",
  "body_text": "string",
  "cta_text": "string",
  "full_text": "string",
  "word_count": 150,
  "quality_score": 0.87,
  "is_approved": false,
  "model_used": "gpt-4o",
  "prompt_version": "v1.2",
  "scene_breakdown": [
    {
      "scene_index": 0,
      "description": "Opening hook with surprising statistic",
      "duration_sec": 5.0,
      "visual_style": "dynamic text overlay on abstract background",
      "voiceover_text": "Did you know...",
      "image_prompt": "Abstract digital background with glowing data points"
    }
  ],
  "created_at": "2026-07-02T04:00:00Z"
}
```

### VideoObject

```json
{
  "video_id": "uuid",
  "project_id": "uuid",
  "version": 1,
  "status": "ready",
  "duration_sec": 30.5,
  "resolution": "1080x1920",
  "file_size_bytes": 52428800,
  "format": "mp4",
  "fps": 30,
  "bitrate_kbps": 12000,
  "file_path": "s3://shortforge-media/videos/abc123.mp4",
  "thumbnail_path": "s3://shortforge-media/thumbnails/abc123.jpg",
  "preview_url": "https://cdn.shortforge.com/videos/abc123_preview.mp4",
  "created_at": "2026-07-02T04:00:00Z"
}
```

### JobStatus Object

```json
{
  "job_id": "uuid",
  "job_type": "video",
  "status": "running",
  "progress_pct": 45,
  "worker_id": "worker-x7g3",
  "started_at": "2026-07-02T04:00:00Z",
  "estimated_completion": "2026-07-02T04:02:00Z",
  "error_message": null
}
```

### CaptionStyleConfig

```json
{
  "font": "Inter",
  "font_size": 48,
  "color": "#FFFFFF",
  "highlight_color": "#FFD700",
  "background_color": "#00000080",
  "position": "bottom_center",
  "max_lines": 2,
  "word_by_word_highlight": true,
  "highlight_delay_ms": 200
}