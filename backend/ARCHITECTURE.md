# ShortForge Architecture

> Last Updated: 2026-07-05

---

# Vision

ShortForge is an AI-powered platform for generating complete short-form video content.

A single request should eventually produce:

- Script
- Title
- Hook
- Thumbnail Prompt
- Images
- Voice
- Subtitles
- Final Rendered Video
- Export-ready files

The backend is designed to remain extensible as new AI providers and media generation features are added.

---

# High Level Architecture

```
                FastAPI
                   │
            API / Routes
                   │
            Dependencies
                   │
          Workflow Layer
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 ScriptService ImageService VoiceService
      │            │            │
      └──────┬─────┴────────────┘
             ▼
         AIService
      ┌──────┴──────────┐
      ▼                 ▼
 Text Provider    Image Provider
      │                 │
 Gemini/OpenAI   Pollinations/Gemini

Repositories
      │
      ▼
 PostgreSQL
```

---

# Project Structure

```
app/

api/
dependencies/
providers/
repositories/
services/
workflows/
schemas/
db/
middleware/
core/
prompts/
```

---

# Responsibilities

## API

Responsible only for:

- receiving requests
- validating input
- returning responses

Must never contain business logic.

---

## Dependencies

Responsible for creating application objects.

Examples:

- AIService
- ProjectService
- ImageService
- Workflow

---

## Workflow

Responsible for orchestration.

A workflow decides:

- what happens first
- what happens next
- how services work together

Workflow does NOT implement business logic.

---

## Services

Responsible for business logic.

Each service should solve one problem only.

Examples:

ScriptService

- generate script

ImageService

- generate images

ProjectService

- manage projects

GeneratedImageService

- manage generated images

---

## Repository

Responsible only for database operations.

Repositories never contain business rules.

---

## Providers

Responsible for talking to external AI providers.

Examples:

Text

- Gemini
- OpenAI
- OpenRouter

Image

- Pollinations
- Gemini

Providers know nothing about FastAPI,
Database,
Repositories,
or Project models.

---

# Current AI Providers

## Text

Current

- Gemini

Planned

- OpenAI
- OpenRouter

---

## Image

Current

- Pollinations
- Gemini

---

# Current Features

Completed

- Project persistence
- SQLAlchemy models
- Alembic migrations
- Repository layer
- Service layer
- AI abstraction
- Text generation
- Image generation
- Local image storage
- Static image serving

---

# Coding Rules

## API

Must never access the database directly.

---

## Service

Should solve one business problem.

---

## Repository

Database only.

No business logic.

---

## Workflow

Coordinates multiple services.

---

## Provider

Communicates with external AI only.

---

## Schema

Represents API contracts.

Schemas are not database models.

---

# Dependency Flow

```
API
↓

Dependencies
↓

Workflow
↓

Services
↓

Repositories
↓

Database
```

---

# Current Workflow

```
Generate Script

↓

Save Project

↓

Generate Images

↓

Save Images

↓

Return Response
```

Future:

```
Generate Script

↓

Generate Images

↓

Generate Thumbnail

↓

Generate Voice

↓

Generate Captions

↓

Render Video

↓

Export

↓

Publish
```

---

# Decision Log

## Decision 001

Separated Text Provider from Image Provider.

Reason:

Different providers may be used independently.

---

## Decision 002

Introduced Repository layer.

Reason:

Separate persistence from business logic.

---

## Decision 003

Introduced Workflow layer.

Reason:

Separate orchestration from business logic.

---

# Development Principles

- Keep services focused.
- Keep providers isolated.
- Keep workflows readable.
- Prefer composition over inheritance.
- Avoid circular dependencies.
- Make adding new AI providers require minimal changes.

---

# Current Milestone

✅ AI Architecture

✅ Database

✅ Project Persistence

✅ Image Generation

🚧 Generation Workflow

---

# Next Milestones

- Complete Generation Workflow
- Voice Generation
- Subtitle Generation
- Video Rendering
- FFmpeg Integration
- Export System
- YouTube Publishing
- TikTok Publishing

---

# Long-Term Goal

One API request should generate a complete short-form video ready for publishing.