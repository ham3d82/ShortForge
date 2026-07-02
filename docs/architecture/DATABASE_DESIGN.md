# ShortForge — Database Design

> **Author**: Principal Software Architect  
> **Version**: 1.0.0  
> **Last Updated**: 2026-07-02

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Entity Relationship Diagram](#2-entity-relationship-diagram)
3. [Table Definitions](#3-table-definitions)
4. [Index Strategy](#4-index-strategy)
5. [Migration Strategy](#5-migration-strategy)
6. [Data Lifecycle](#6-data-lifecycle)
7. [Performance Considerations](#7-performance-considerations)
8. [Backup & Recovery](#8-backup--recovery)

---

## 1. Design Philosophy

### Guiding Principles

| Principle | Implementation |
|-----------|---------------|
| **Normalization** | 3NF for transactional data; denormalized read models for queries |
| **UUID Primary Keys** | Distributed-friendly, no sequential leaks, merge-safe |
| **Soft Deletes** | All entities use `deleted_at` timestamp for audit trail |
| **Audit Trail** | `created_at`, `updated_at` on all tables; separate audit log for mutations |
| **JSONB for Flexibility** | Extensible metadata fields without schema changes |
| **Enum as Strings** | Human-readable in DB, validated at application layer with Pydantic |
| **Cascade Carefully** | Prefer application-level cascade over DB-level for control |

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Tables | `snake_case`, plural | `users`, `video_projects` |
| Columns | `snake_case`, singular | `created_at`, `user_id` |
| Primary Keys | `{table}_id` | `user_id`, `project_id` |
| Foreign Keys | `{referenced_table}_id` | `project_id`, `script_id` |
| Indexes | `idx_{table}_{column}` | `idx_users_email` |
| Unique Constraints | `uq_{table}_{column}` | `uq_users_email` |
| Junction Tables | `{table1}_{table2}` | `project_tags` |

---

## 2. Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ShortForge Database Schema                          │
│                                                                              │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────────┐       │
│  │    users      │    │  video_projects  │    │     scripts          │       │
│  ├──────────────┤    ├──────────────────┤    ├──────────────────────┤       │
│  │ user_id (PK) │──┐ │ project_id (PK)  │──┐ │ script_id (PK)       │       │
│  │ email        │  │ │ user_id (FK)     │  │ │ project_id (FK)      │       │
│  │ password_hash│  │ │ title            │  ├─│ version              │       │
│  │ display_name │  │ │ topic            │  │ │ status (enum)        │       │
│  │ role (enum)  │  │ │ tone (enum)      │  │ │ hook_text            │       │
│  │ avatar_url   │  │ │ target_duration  │  │ │ body_text            │       │
│  │ is_active    │  │ │ language         │  │ │ cta_text             │       │
│  │ created_at   │  │ │ status (enum)    │  │ │ full_text            │       │
│  │ updated_at   │  │ │ metadata (JSONB) │  │ │ scene_breakdown(JSONB)│      │
│  │ deleted_at   │  │ │ created_at       │  │ │ word_count           │       │
│  └──────────────┘  │ │ updated_at       │  │ │ quality_score        │       │
│       │            │ │ deleted_at       │  │ │ is_approved          │       │
│       │            │ └──────────────────┘  │ │ approved_by          │       │
│       │            │        │              │ │ created_at           │       │
│       │            │        │              │ │ updated_at           │       │
│       │            │        │              │ │ deleted_at           │       │
│       │            │        │              │ │ parent_script_id(FK) │       │
│       │            │        │              │ └──────────┬───────────┘       │
│       │            │        │              │            │                    │
│       ▼            │        │              │            │                    │
│  ┌──────────┐      │        ▼              │            ▼                    │
│  │ youtube_ │      │  ┌────────────────┐   │  ┌──────────────────────┐      │
│  │ accounts │      │  │ project_media  │   │  │  project_tags        │      │
│  ├──────────┤      │  ├────────────────┤   │  ├──────────────────────┤      │
│  │ account_ │      │  │ media_id (PK)  │   │  │ project_id (FK)      │      │
│  │ id (PK)  │      ├──│ project_id(FK) │   │  │ tag (text)           │      │
│  │ user_id  │      │  │ file_type(enum)│   │  │ created_at           │      │
│  │ provider │      │  │ storage_path   │   │  └──────────────────────┘      │
│  │ provider │      │  │ original_name  │   │                                │
│  │ _user_id │      │  │ mime_type      │   │  ┌──────────────────────┐      │
│  │ access_  │      │  │ file_size      │   │  │ project_keywords     │      │
│  │ token    │      │  │ metadata(JSONB)│   │  ├──────────────────────┤      │
│  │ refresh_ │      │  │ created_at     │   │  │ project_id (FK)      │      │
│  │ token    │      │  └────────────────┘   │  │ keyword (text)       │      │
│  │ token_   │      │        │              │  │ created_at           │      │
│  │ expires  │      │        │              │  └──────────────────────┘      │
│  │ scopes   │      │        │              │                                │
│  │ created_ │      │        ▼              │                                │
│  │ at       │      │  ┌────────────────┐   │                                │
│  │ updated_ │      │  │  voiceovers    │   │                                │
│  │ at       │      │  ├────────────────┤   │                                │
│  └──────────┘      │  │ voiceover_id   │   │                                │
│       │            ├──│ project_id(FK) │   │                                │
│       │            │  │ script_id (FK) │   │                                │
│       │            │  │ provider (enum)│   │                                │
│       ▼            │  │ voice_id       │   │                                │
│  ┌────────────┐    │  │ audio_file_path│   │                                │
│  │ user_sessions│   │  │ duration_ms    │   │                                │
│  ├────────────┤    │  │ silence_       │   │                                │
│  │ session_id │    │  │ inserted(JSONB)│   │                                │
│  │ user_id    │    │  │ timing_meta   │   │                                │
│  │ token_hash │    │  │ (JSONB)        │   │                                │
│  │ ip_address │    │  │ status (enum)  │   │                                │
│  │ user_agent │    │  │ language       │   │                                │
│  │ expires_at │    │  │ created_at     │   │                                │
│  │ created_at │    │  │ updated_at     │   │                                │
│  └────────────┘    │  └────────────────┘   │                                │
│                    │        │              │                                │
│                    │        │              │                                │
│                    │        ▼              │                                │
│                    │  ┌────────────────┐   │  ┌──────────────────────┐      │
│                    │  │  subtitles     │   │  │    images            │      │
│                    │  ├────────────────┤   │  ├──────────────────────┤      │
│                    ├──│ subtitle_id(PK)│   ├──│ image_id (PK)        │      │
│                    │  │ voiceover_id   │   │  │ project_id (FK)      │      │
│                    │  │ script_id (FK) │   │  │ script_id (FK)       │      │
│                    │  │ format (enum)  │   │  │ scene_index          │      │
│                    │  │ srt_content    │   │  │ provider (enum)      │      │
│                    │  │ ass_content    │   │  │ prompt_text          │      │
│                    │  │ word_timestamps│   │  │ image_file_path      │      │
│                    │  │ (JSONB)        │   │  │ style (enum)         │      │
│                    │  │ language       │   │  │ upscaled_path        │      │
│                    │  │ created_at     │   │  │ animated_path        │      │
│                    │  │ updated_at     │   │  │ status (enum)        │      │
│                    │  └────────────────┘   │  │ width                │      │
│                    │        │              │  │ height               │      │
│                    │        │              │  │ metadata (JSONB)     │      │
│                    │        │              │  │ created_at           │      │
│                    │        │              │  │ updated_at           │      │
│                    │        ▼              │  └──────────────────────┘      │
│                    │  ┌────────────────┐   │                                │
│                    │  │   videos       │   │                                │
│                    │  ├────────────────┤   │                                │
│                    ├──│ video_id (PK)  │   │                                │
│                    │  │ project_id(FK) │   │                                │
│                    │  │ script_id (FK) │   │                                │
│                    │  │ voiceover_id   │   │                                │
│                    │  │ status (enum)  │   │                                │
│                    │  │ file_path      │   │                                │
│                    │  │ thumbnail_path │   │                                │
│                    │  │ duration_sec   │   │                                │
│                    │  │ resolution     │   │                                │
│                    │  │ file_size_bytes│   │                                │
│                    │  │ format (enum)  │   │                                │
│                    │  │ fps            │   │                                │
│                    │  │ bitrate_kbps   │   │                                │
│                    │  │ metadata (JSONB)│  │                                │
│                    │  │ rendered_by    │   │                                │
│                    │  │ render_started │   │                                │
│                    │  │ render_completed│  │                                │
│                    │  │ error_message  │   │                                │
│                    │  │ created_at     │   │                                │
│                    │  │ updated_at     │   │                                │
│                    │  └────────────────┘   │                                │
│                    │        │              │                                │
│                    │        ▼              │                                │
│                    │  ┌────────────────┐   │                                │
│                    │  │  publications  │   │                                │
│                    │  ├────────────────┤   │                                │
│                    ├──│ publish_id(PK) │   │                                │
│                    │  │ video_id (FK)  │   │                                │
│                    │  │ account_id (FK)│   │                                │
│                    │  │ status (enum)  │   │                                │
│                    │  │ youtube_video  │   │                                │
│                    │  │ _id            │   │                                │
│                    │  │ title          │   │                                │
│                    │  │ description    │   │                                │
│                    │  │ tags (text[])  │   │                                │
│                    │  │ category_id    │   │                                │
│                    │  │ visibility     │   │                                │
│                    │  │ (enum)         │   │                                │
│                    │  │ scheduled_for  │   │                                │
│                    │  │ published_at   │   │                                │
│                    │  │ error_message  │   │                                │
│                    │  │ retry_count    │   │                                │
│                    │  │ created_at     │   │                                │
│                    │  │ updated_at     │   │                                │
│                    │  │ deleted_at     │   │                                │
│                    │  └────────────────┘   │                                │
│                    │        │              │                                │
│                    │        │              │                                │
│                    │        ▼              │                                │
│                    │  ┌────────────────┐   │  ┌──────────────────────┐      │
│                    │  │  audit_log     │   │  │   generation_jobs    │      │
│                    │  ├────────────────┤   │  ├──────────────────────┤      │
│                    │  │ log_id (PK)    │   │  │ job_id (PK)          │      │
│                    │  │ entity_type    │   ├──│ project_id (FK)      │      │
│                    │  │ entity_id (UUID)│  │  │ job_type (enum)      │      │
│                    │  │ action (enum)  │   │  │ status (enum)        │      │
│                    │  │ old_values     │   │  │ worker_id            │      │
│                    │  │ (JSONB)        │   │  │ queue_name           │      │
│                    │  │ new_values     │   │  │ celery_task_id       │      │
│                    │  │ (JSONB)        │   │  │ progress_pct         │      │
│                    │  │ actor_id (FK)  │   │  │ started_at           │      │
│                    │  │ ip_address     │   │  │ completed_at         │      │
│                    │  │ created_at     │   │  │ error_message        │      │
│                    │  └────────────────┘   │  │ retry_count          │      │
│                    │        │              │  │ max_retries          │      │
│                    │        │              │  │ metadata (JSONB)     │      │
│                    │        │              │  │ created_at           │      │
│                    │        │              │  │ updated_at           │      │
│                    │        │              │  └──────────────────────┘      │
│                    ▼        ▼              │                                │
│              ┌────────────────────────────┐│                                │
│              │  settings / config         ││                                │
│              ├────────────────────────────┤│                                │
│              │ setting_id (PK)            ││                                │
│              │ user_id (FK, nullable)     ││                                │
│              │ key (varchar)              ││                                │
│              │ value (JSONB)              ││                                │
│              │ scope (enum)               ││                                │
│              │ created_at                 ││                                │
│              │ updated_at                 ││                                │
│              └────────────────────────────┘│                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Table Definitions

### 3.1 `users` — Platform Users

```sql
CREATE TABLE users (
    user_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    display_name    VARCHAR(100) NOT NULL,
    role            VARCHAR(20) NOT NULL DEFAULT 'creator'
                        CHECK (role IN ('creator', 'premium', 'admin')),
    avatar_url      VARCHAR(512),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    preferences     JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE UNIQUE INDEX uq_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role) WHERE deleted_at IS NULL;
```

### 3.2 `user_sessions` — Auth Sessions

```sql
CREATE TABLE user_sessions (
    session_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash      VARCHAR(255) NOT NULL,
    ip_address      INET,
    user_agent      TEXT,
    expires_at      TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_expires ON user_sessions(expires_at) WHERE expires_at > NOW();
CREATE UNIQUE INDEX uq_sessions_token ON user_sessions(token_hash);
```

### 3.3 `youtube_accounts` — Connected YouTube Channels

```sql
CREATE TABLE youtube_accounts (
    account_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    provider         VARCHAR(20) NOT NULL DEFAULT 'google',
    provider_user_id VARCHAR(255) NOT NULL,
    channel_name     VARCHAR(255),
    channel_id       VARCHAR(255),
    access_token     TEXT NOT NULL,
    refresh_token    TEXT,
    token_expires_at TIMESTAMPTZ,
    scopes           TEXT[],
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX uq_youtube_provider ON youtube_accounts(provider, provider_user_id);
CREATE INDEX idx_youtube_user ON youtube_accounts(user_id);
```

### 3.4 `video_projects` — Generation Projects (Core Entity)

```sql
CREATE TABLE video_projects (
    project_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title           VARCHAR(255),
    topic           TEXT NOT NULL,
    tone            VARCHAR(50) NOT NULL DEFAULT 'educational'
                        CHECK (tone IN ('educational', 'humorous', 'inspirational',
                                        'entertaining', 'dramatic', 'controversial')),
    target_duration INT NOT NULL DEFAULT 30
                        CHECK (target_duration BETWEEN 15 AND 180),
    language        VARCHAR(10) NOT NULL DEFAULT 'en',
    status          VARCHAR(30) NOT NULL DEFAULT 'draft'
                        CHECK (status IN ('draft', 'script_generating', 'script_ready',
                                          'script_approved', 'generating', 'ready',
                                          'failed', 'archived')),
    generation_progress JSONB DEFAULT '{}'::JSONB,
    metadata        JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_projects_user ON video_projects(user_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_status ON video_projects(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_created ON video_projects(created_at DESC) WHERE deleted_at IS NULL;
```

### 3.5 `scripts` — Generated Scripts

```sql
CREATE TABLE scripts (
    script_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    version         INT NOT NULL DEFAULT 1,
    status          VARCHAR(30) NOT NULL DEFAULT 'generating'
                        CHECK (status IN ('generating', 'ready', 'approved', 'rejected')),
    hook_text       TEXT,
    body_text       TEXT,
    cta_text        TEXT,
    full_text       TEXT NOT NULL,
    scene_breakdown JSONB DEFAULT '[]'::JSONB,
        -- Array of: { "scene_index": int, "description": str, "duration_sec": float,
        --             "visual_style": str, "voiceover_text": str, "image_prompt": str }
    word_count      INT,
    quality_score   FLOAT CHECK (quality_score BETWEEN 0 AND 1),
    is_approved     BOOLEAN NOT NULL DEFAULT FALSE,
    approved_by     UUID REFERENCES users(user_id),
    approved_at     TIMESTAMPTZ,
    model_used      VARCHAR(100),
    prompt_version  VARCHAR(50),
    metadata        JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ,
    parent_script_id UUID REFERENCES scripts(script_id)
        -- Links edited versions to their original
);

CREATE INDEX idx_scripts_project ON scripts(project_id);
CREATE INDEX idx_scripts_status ON scripts(status);
CREATE INDEX idx_scripts_approved ON scripts(project_id, is_approved) WHERE is_approved = TRUE;
```

### 3.6 `project_tags` — Tags for Organization

```sql
CREATE TABLE project_tags (
    project_id  UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    tag         VARCHAR(50) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (project_id, tag)
);

CREATE INDEX idx_tags_tag ON project_tags(tag);
```

### 3.7 `project_keywords` — SEO Keywords

```sql
CREATE TABLE project_keywords (
    project_id  UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    keyword     VARCHAR(100) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (project_id, keyword)
);
```

### 3.8 `project_media` — Uploaded/Generated Media Files

```sql
CREATE TABLE project_media (
    media_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    file_type       VARCHAR(20) NOT NULL
                        CHECK (file_type IN ('background_video', 'background_image',
                                             'logo', 'music', 'font', 'other')),
    storage_backend VARCHAR(20) NOT NULL DEFAULT 's3',
    storage_path    VARCHAR(512) NOT NULL,
    original_name   VARCHAR(255),
    mime_type       VARCHAR(100),
    file_size_bytes BIGINT,
    width           INT,
    height          INT,
    duration_sec    FLOAT,
    metadata        JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_media_project ON project_media(project_id);
CREATE INDEX idx_media_type ON project_media(file_type);
```

### 3.9 `voiceovers` — TTS Audio Files

```sql
CREATE TABLE voiceovers (
    voiceover_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id        UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    script_id         UUID REFERENCES scripts(script_id),
    provider          VARCHAR(30) NOT NULL
                          CHECK (provider IN ('elevenlabs', 'azure', 'amazon', 'google', 'local')),
    voice_id          VARCHAR(100) NOT NULL,
    voice_name        VARCHAR(100),
    audio_file_path   VARCHAR(512) NOT NULL,
    duration_ms       INT NOT NULL,
    silence_inserted  JSONB DEFAULT '[]'::JSONB,
        -- Array of: { "position_ms": int, "duration_ms": int }
    timing_metadata   JSONB DEFAULT '{}'::JSONB,
        -- { "segments": [{"start_ms": int, "end_ms": int, "text": str}], "total_ms": int }
    status            VARCHAR(20) NOT NULL DEFAULT 'generating'
                          CHECK (status IN ('generating', 'ready', 'failed')),
    language          VARCHAR(10) NOT NULL DEFAULT 'en',
    speed_multiplier  FLOAT NOT NULL DEFAULT 1.0,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_voiceovers_project ON voiceovers(project_id);
CREATE INDEX idx_voiceovers_script ON voiceovers(script_id);
```

### 3.10 `images` — Generated Images

```sql
CREATE TABLE images (
    image_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    script_id       UUID REFERENCES scripts(script_id),
    scene_index     INT NOT NULL DEFAULT 0,
    provider        VARCHAR(30) NOT NULL
                        CHECK (provider IN ('stability', 'openai', 'midjourney', 'flux', 'local')),
    prompt_text     TEXT NOT NULL,
    negative_prompt TEXT,
    style           VARCHAR(50) DEFAULT 'realistic',
    image_file_path VARCHAR(512) NOT NULL,
    upscaled_path   VARCHAR(512),
    animated_path   VARCHAR(512),
    status          VARCHAR(20) NOT NULL DEFAULT 'generating'
                        CHECK (status IN ('generating', 'generated', 'upscaled',
                                          'animated', 'failed')),
    width           INT DEFAULT 1080,
    height          INT DEFAULT 1920,
    seed            BIGINT,
    inference_steps INT DEFAULT 30,
    guidance_scale  FLOAT DEFAULT 7.0,
    animation_frames INT DEFAULT 0,
    metadata        JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_images_project ON images(project_id);
CREATE INDEX idx_images_scene ON images(project_id, scene_index);
CREATE INDEX idx_images_status ON images(status);
```

### 3.11 `subtitles` — Caption Files

```sql
CREATE TABLE subtitles (
    subtitle_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    voiceover_id    UUID REFERENCES voiceovers(voiceover_id) ON DELETE SET NULL,
    script_id       UUID NOT NULL REFERENCES scripts(script_id) ON DELETE CASCADE,
    format          VARCHAR(10) NOT NULL DEFAULT 'srt'
                        CHECK (format IN ('srt', 'ass', 'vtt')),
    language        VARCHAR(10) NOT NULL DEFAULT 'en',
    original_language VARCHAR(10) NOT NULL DEFAULT 'en',
    srt_content     TEXT,
    ass_content     TEXT,
    word_timestamps JSONB NOT NULL DEFAULT '[]'::JSONB,
        -- Array of: { "word": str, "start_ms": int, "end_ms": int, "confidence": float }
    style_config    JSONB DEFAULT '{}'::JSONB,
        -- { "font": str, "font_size": int, "color": str, "position": str,
        --   "highlight_color": str, "background_color": str }
    source          VARCHAR(20) NOT NULL DEFAULT 'whisper'
                        CHECK (source IN ('whisper', 'manual', 'translated')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_subtitles_voiceover ON subtitles(voiceover_id);
CREATE INDEX idx_subtitles_script ON subtitles(script_id);
```

### 3.12 `videos` — Rendered Videos

```sql
CREATE TABLE videos (
    video_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id       UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    script_id        UUID REFERENCES scripts(script_id),
    voiceover_id     UUID REFERENCES voiceovers(voiceover_id),
    status           VARCHAR(30) NOT NULL DEFAULT 'pending'
                         CHECK (status IN ('pending', 'rendering', 'ready',
                                           'failed', 'archived')),
    version          INT NOT NULL DEFAULT 1,
    file_path        VARCHAR(512),
    thumbnail_path   VARCHAR(512),
    duration_sec     FLOAT,
    resolution       VARCHAR(20) DEFAULT '1080x1920',
    file_size_bytes  BIGINT,
    format           VARCHAR(10) NOT NULL DEFAULT 'mp4'
                         CHECK (format IN ('mp4', 'webm', 'mov')),
    fps              INT DEFAULT 30,
    bitrate_kbps     INT,
    codec            VARCHAR(20) DEFAULT 'h264',
    encoder          VARCHAR(50) DEFAULT 'libx264',
    metadata         JSONB DEFAULT '{}'::JSONB,
    rendered_by      VARCHAR(100),
    render_started   TIMESTAMPTZ,
    render_completed TIMESTAMPTZ,
    error_message    TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_videos_project ON videos(project_id);
CREATE INDEX idx_videos_status ON videos(status);
CREATE UNIQUE INDEX uq_videos_project_version ON videos(project_id, version);
```

### 3.13 `publications` — YouTube Publishing Records

```sql
CREATE TABLE publications (
    publish_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    video_id        UUID NOT NULL REFERENCES videos(video_id) ON DELETE CASCADE,
    account_id      UUID NOT NULL REFERENCES youtube_accounts(account_id) ON DELETE CASCADE,
    status          VARCHAR(30) NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'uploading', 'uploaded', 'published',
                                          'scheduled', 'failed', 'deleted')),
    youtube_video_id VARCHAR(255),
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    tags            TEXT[],
    category_id     VARCHAR(20),
    visibility      VARCHAR(20) NOT NULL DEFAULT 'unlisted'
                        CHECK (visibility IN ('public', 'unlisted', 'private')),
    scheduled_for   TIMESTAMPTZ,
    published_at    TIMESTAMPTZ,
    error_message   TEXT,
    retry_count     INT NOT NULL DEFAULT 0,
    max_retries     INT NOT NULL DEFAULT 3,
    youtube_metadata JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_publishes_video ON publications(video_id);
CREATE INDEX idx_publishes_account ON publications(account_id);
CREATE INDEX idx_publishes_status ON publications(status);
CREATE INDEX idx_publishes_scheduled ON publications(scheduled_for)
    WHERE status = 'scheduled' AND scheduled_for > NOW();
```

### 3.14 `generation_jobs` — Celery Task Tracking

```sql
CREATE TABLE generation_jobs (
    job_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES video_projects(project_id) ON DELETE CASCADE,
    job_type        VARCHAR(30) NOT NULL
                        CHECK (job_type IN ('script', 'audio', 'image', 'animation',
                                            'caption', 'video', 'thumbnail', 'publish')),
    status          VARCHAR(20) NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'running', 'completed', 'failed', 'retrying')),
    worker_id       VARCHAR(100),
    queue_name      VARCHAR(100),
    celery_task_id  VARCHAR(255),
    progress_pct    INT DEFAULT 0 CHECK (progress_pct BETWEEN 0 AND 100),
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    error_message   TEXT,
    retry_count     INT NOT NULL DEFAULT 0,
    max_retries     INT NOT NULL DEFAULT 3,
    metadata        JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_jobs_project ON generation_jobs(project_id);
CREATE INDEX idx_jobs_status ON generation_jobs(status);
CREATE INDEX idx_jobs_type_status ON generation_jobs(job_type, status);
CREATE INDEX idx_jobs_created ON generation_jobs(created_at DESC);
```

### 3.15 `audit_log` — Immutable Audit Trail

```sql
CREATE TABLE audit_log (
    log_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     VARCHAR(50) NOT NULL,
    entity_id       UUID NOT NULL,
    action          VARCHAR(30) NOT NULL
                        CHECK (action IN ('created', 'updated', 'deleted', 'restored',
                                          'approved', 'rejected', 'generated', 'published',
                                          'failed', 'retried')),
    old_values      JSONB,
    new_values      JSONB,
    changed_fields  TEXT[],
    actor_id        UUID REFERENCES users(user_id),
    ip_address      INET,
    user_agent      TEXT,
    correlation_id  UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE audit_log_2026_01 PARTITION OF audit_log
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE audit_log_2026_02 PARTITION OF audit_log
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
-- ... automated via pg_partman or Alembic

CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_actor ON audit_log(actor_id);
CREATE INDEX idx_audit_created ON audit_log(created_at DESC);
CREATE INDEX idx_audit_correlation ON audit_log(correlation_id);
```

### 3.16 `settings` — User & System Configuration

```sql
CREATE TABLE settings (
    setting_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID REFERENCES users(user_id) ON DELETE CASCADE,
    key         VARCHAR(100) NOT NULL,
    value       JSONB NOT NULL DEFAULT '{}'::JSONB,
    scope       VARCHAR(20) NOT NULL DEFAULT 'user'
                    CHECK (scope IN ('system', 'user', 'project')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, key)
);

CREATE INDEX idx_settings_user ON settings(user_id);
CREATE INDEX idx_settings_key ON settings(key);
```

---

## 4. Index Strategy

### 4.1 Index Categories

| Category | Strategy | Examples |
|----------|----------|----------|
| **Primary Lookup** | B-tree on UUID PK | All `*_id` columns |
| **Foreign Key** | B-tree on FK columns | `project_id`, `user_id` |
| **Filter Query** | B-tree on status/type | `status`, `job_type` |
| **Sort Order** | B-tree DESC on timestamps | `created_at DESC` |
| **Unique Constraint** | UNIQUE index with WHERE | `uq_users_email` with soft delete |
| **Full-Text Search** | GIN on tsvector | Future: `scripts.full_text` |
| **JSON Queries** | GIN on JSONB | `metadata`, `word_timestamps` |

### 4.2 Coverage Analysis

| Query Pattern | Tables | Indexes Used |
|---------------|--------|--------------|
| Load user's projects | `video_projects` | `idx_projects_user`, `idx_projects_created` |
| Find active project | `video_projects` | `idx_projects_user` + `idx_projects_status` |
| Get latest script | `scripts` | `idx_scripts_project` + `created_at` |
| Find pending jobs | `generation_jobs` | `idx_jobs_type_status` |
| Get project images | `images` | `idx_images_project` |
| Check scheduled publishes | `publications` | `idx_publishes_scheduled` |
| Audit trail by entity | `audit_log` | `idx_audit_entity` + partitioning |

### 4.3 Partial Indexes

```sql
-- Only index active (non-deleted) records
CREATE INDEX idx_projects_active ON video_projects(project_id, user_id)
    WHERE deleted_at IS NULL AND status != 'archived';

-- Only index pending/running jobs for worker polling
CREATE INDEX idx_jobs_pending ON generation_jobs(job_type, created_at)
    WHERE status IN ('pending', 'retrying');

-- Only index approved scripts for generation
CREATE INDEX idx_scripts_approved ON scripts(project_id)
    WHERE is_approved = TRUE AND deleted_at IS NULL;

-- Only index future scheduled publications
CREATE INDEX idx_scheduled_future ON publications(scheduled_for)
    WHERE status = 'scheduled' AND scheduled_for > NOW();
```

---

## 5. Migration Strategy

### 5.1 Tool: Alembic

```
backend/infrastructure/db/
├── migrations/
│   ├── env.py                  # Alembic environment config
│   ├── alembic.ini             # Alembic configuration
│   ├── script.py.mako          # Migration template
│   └── versions/               # Generated migration files
│       ├── 0001_initial_schema.py
│       ├── 0002_add_youtube_accounts.py
│       └── ...
├── models/                     # SQLAlchemy ORM models
└── base.py                     # Declarative Base
```

### 5.2 Migration Principles

1. **One Change Per Migration**: Each migration does exactly one thing (add table, add column, add index)
2. **Both Directions**: Always implement `upgrade()` AND `downgrade()` 
3. **Data Migrations**: Split schema changes from data migrations (separate scripts)
4. **Zero-Downtime**: Follow this pattern for production:

```python
# Step 1: Add new column as nullable
def upgrade():
    op.add_column('videos', sa.Column('new_column', sa.String(), nullable=True))

# Step 2: Backfill data (separate migration or script)
# ...

# Step 3: Make column NOT NULL
def upgrade():
    op.alter_column('videos', 'new_column', nullable=False)
```

5. **Naming Convention**: `{YYYY}_{MM}_{DD}_{seq}_{description}.py`
   - Example: `2026_07_02_0001_create_users_table.py`

### 5.3 Initial Schema Migration Order

```
1. Create users, user_sessions
2. Create youtube_accounts
3. Create video_projects
4. Create scripts, project_tags, project_keywords
5. Create project_media
6. Create voiceovers
7. Create images
8. Create subtitles
9. Create videos
10. Create publications
11. Create generation_jobs
12. Create audit_log (with partitions)
13. Create settings
14. Seed data (admin user, default settings)
```

---

## 6. Data Lifecycle

### 6.1 Retention Policies

| Entity | Retention | Action |
|--------|-----------|--------|
| **Active Projects** | Indefinite | Keep accessible |
| **Archived Projects** | 90 days after archive | Soft delete → hard delete |
| **Generated Videos** | 30 days after creation (unpublished) | Soft delete; keep metadata |
| **Published Videos** | Indefinite (reference only) | Keep record, delete local file |
| **Audit Logs** | 1 year | Partitioned; drop old partitions |
| **User Sessions** | Until expiry | Auto-delete on expiry |
| **Temp Media** | 24 hours | Cleanup via Celery Beat |
| **Deleted Users** | 30 days | GDPR window → anonymize |

### 6.2 Cleanup Tasks (Celery Beat)

```python
# Scheduled tasks (crontab)
CELERY_BEAT_SCHEDULE = {
    'cleanup-expired-sessions': {
        'task': 'cleanup.expired_sessions',
        'schedule': crontab(hour='*/1'),  # Every hour
    },
    'cleanup-temp-media': {
        'task': 'cleanup.temp_media',
        'schedule': crontab(hour='3', minute='0'),  # Daily at 3 AM
    },
    'archive-stale-projects': {
        'task': 'cleanup.archive_stale_projects',
        'schedule': crontab(hour='2', minute='0'),  # Daily at 2 AM
    },
    'hard-delete-archived': {
        'task': 'cleanup.hard_delete_archived',
        'schedule': crontab(hour='4', minute='0', day_of_week='0'),  # Weekly Sunday
    },
    'drop-old-audit-partitions': {
        'task': 'cleanup.drop_audit_partitions',
        'schedule': crontab(day_of_month='1', hour='5'),  # Monthly
    },
}
```

---

## 7. Performance Considerations

### 7.1 Connection Pooling

```python
# SQLAlchemy async engine configuration
DATABASE_CONFIG = {
    "pool_size": 20,              # Base connections
    "max_overflow": 10,           # Additional connections under load
    "pool_timeout": 30,           # Wait time for a connection
    "pool_recycle": 1800,         # Recycle connections after 30 min
    "pool_pre_ping": True,        # Verify connection before use
    "echo_pool": False,           # Log pool state (dev only)
}
```

### 7.2 Query Optimization Rules

1. **N+1 Prevention**: Always use `selectinload()` or `joinedload()` for relationships
2. **Pagination**: Use keyset pagination (`WHERE id > $1 LIMIT 50`) over OFFSET for large datasets
3. **Batch Operations**: Use `bulk_insert()` and `bulk_update()` for batch saves
4. **Read Models**: Create materialized views for complex dashboard queries
5. **JSONB Queries**: Use GIN indexes for `@>`, `?`, `?|` operators
6. **Full-Text Search**: Add `tsvector` column with GIN index for script search

### 7.3 Connection Limits by Component

| Component | Max Connections | Reason |
|-----------|----------------|--------|
| API Server (x4 pods) | 80 (20 each) | Primary workload |
| Celery Workers (x8) | 40 (5 each) | Batch operations |
| Celery Beat | 2 | Occasional cleanup |
| Migration Runner | 5 | Schema changes |
| Alembic | 1 | Exclusive lock |
| **Total Budget** | **128** | Leave headroom |

---

## 8. Backup & Recovery

### 8.1 Backup Schedule

| Type | Frequency | Retention | Method |
|------|-----------|-----------|--------|
| Full DB | Daily | 30 days | `pg_dump -Fc` |
| WAL Archiving | Continuous | 7 days | `pg_archive` |
| Logical Backup | Weekly | 90 days | `pg_dump --schema-only` |
| Media Files | Daily | 30 days | S3 versioning |

### 8.2 Recovery Time Objectives

| Scenario | RTO | RPO |
|----------|-----|-----|
| Accidental data loss | 1 hour | 5 minutes |
| DB corruption | 4 hours | 24 hours (daily backup) |
| Full region outage | 8 hours | 1 hour |
| Media corruption | 1 hour | 24 hours |

### 8.3 Disaster Recovery Playbook

```bash
# Full restore from daily backup
pg_restore -d shortforge -U shortforge \
    --jobs=4 --verbose \
    /backups/shortforge_20260701.dump

# Point-in-time recovery
pg_restore -d shortforge -U shortforge \
    --jobs=4 --verbose \
    --timestamp="2026-07-02 03:00:00 UTC" \
    /backups/shortforge_latest.dump
```

---

## Appendix: Entity State Machine

```
video_projects.status:
  draft ──► script_generating ──► script_ready ──► script_approved ──► generating ──► ready
        │                              │                    │                      │
        └──────────────────────────────┴────────────────────┴──────────────────────┴──► failed

generation_jobs.status:
  pending ──► running ──► completed
       │         │
       └── retrying ──► running ──► completed
                            │
                            └── failed

publications.status:
  pending ──► uploading ──► uploaded ──► published / scheduled
       │          │              │
       └──────────┴──────────────┴──► failed

images.status:
  generating ──► generated ──► upscaled ──► animated
       │
       └── failed
```

---

## Appendix B: Storage Size Estimates

| Table | Row Estimate | Row Size | Total |
|-------|-------------|----------|-------|
| users | 10,000 | ~500 B | 5 MB |
| video_projects | 500,000 | ~1 KB | 500 MB |
| scripts | 1,000,000 | ~10 KB | 10 GB |
| images | 5,000,000 | ~500 B | 2.5 GB |
| voiceovers | 500,000 | ~200 B | 100 MB |
| subtitles | 500,000 | ~50 KB | 25 GB |
| videos | 500,000 | ~200 B | 100 MB |
| publications | 500,000 | ~1 KB | 500 MB |
| generation_jobs | 5,000,000 | ~500 B | 2.5 GB |
| audit_log | 50,000,000 | ~2 KB | 100 GB |
| **Total** | | | **~141 GB** |