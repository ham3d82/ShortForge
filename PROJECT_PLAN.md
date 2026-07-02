# ShortForge — Project Plan

## 🎯 Vision

Build a production-grade, AI-powered YouTube Shorts generator that allows creators to generate, preview, and publish short-form video content with minimal manual effort. The system will be modular, extensible, and deployable via Docker.

---

## 🗺 Milestones & Roadmap

### Phase 1: Foundation (Weeks 1–2)
- [x] Project scaffolding & folder structure
- [ ] Define domain entities & value objects
- [ ] Set up PostgreSQL schema & migrations (Alembic)
- [ ] Implement core config & dependency injection
- [ ] Create FastAPI app skeleton with health check
- [ ] Set up Docker Compose (API, DB, Redis, MinIO)
- [ ] CI/CD pipeline (lint, test, build)

### Phase 2: User & Auth (Weeks 3–4)
- [ ] User registration / login (JWT + refresh tokens)
- [ ] OAuth2 integration (Google / YouTube)
- [ ] User profile & API key management
- [ ] Rate limiting & security middleware

### Phase 3: AI Script Generation (Weeks 5–6)
- [ ] LLM integration layer (OpenAI / Anthropic)
- [ ] Prompt templates & versioning
- [ ] Script generation use case
- [ ] Script editing & approval (frontend)
- [ ] Evaluation & quality scoring

### Phase 4: Media Pipeline (Weeks 7–9)
- [ ] Text-to-Speech (ElevenLabs / Azure TTS)
- [ ] Video assembly engine (FFmpeg / MoviePy)
- [ ] Auto-captioning (Whisper + burn-in)
- [ ] Thumbnail generation
- [ ] Background music & audio mixing

### Phase 5: YouTube Integration (Weeks 10–11)
- [ ] YouTube Data API v3 client
- [ ] Upload, schedule, publish
- [ ] Analytics & performance tracking
- [ ] Error handling & retry logic

### Phase 6: Frontend Dashboard (Weeks 12–14)
- [ ] Project CRUD (create, list, edit, delete)
- [ ] Generation wizard (multi-step form)
- [ ] Preview player (video + captions)
- [ ] Publishing queue & history
- [ ] Responsive design & dark mode

### Phase 7: Production Hardening (Weeks 15–16)
- [ ] Async worker monitoring (Flower / Prometheus)
- [ ] Logging & error tracking (Sentry)
- [ ] Caching strategy (Redis)
- [ ] Load testing & performance optimization
- [ ] Documentation & deployment guide

---

## 🧱 Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend framework | FastAPI | Async, auto-docs, Pydantic validation |
| Frontend framework | React + Vite | Fast HMR, TypeScript-first |
| State management | Zustand | Lightweight, no boilerplate |
| ORM | SQLAlchemy 2.0 | Mature, async support, migrations |
| Task queue | Celery + Redis | Battle-tested, flower monitoring |
| AI orchestration | LangChain | Multi-model, prompt management |
| Video processing | FFmpeg (subprocess) | Most reliable, GPU acceleration |
| Containerization | Docker Compose | Dev/prod parity, easy onboarding |

---

## 📐 Clean Architecture Layers

### Domain Layer (`backend/domain/`)
- **Entities**: `User`, `Project`, `Script`, `Video`, `Voiceover`, `Thumbnail`
- **Value Objects**: `Email`, `YouTubeUrl`, `Duration`, `Resolution`, `Language`
- **Enums**: `ProjectStatus`, `GenerationStatus`, `VideoFormat`, `VoiceStyle`

### Application Layer (`backend/application/`)
- **Use Cases**: `GenerateScript`, `AssembleVideo`, `PublishToYouTube`
- **Services**: `ScriptService`, `VideoService`, `PublishingService`
- **Interfaces (Ports)**: `IScriptRepository`, `IVideoRepository`, `IAIService`
- **DTOs**: `CreateProjectDTO`, `GenerateScriptDTO`, `PublishVideoDTO`

### Infrastructure Layer (`backend/infrastructure/`)
- **DB**: SQLAlchemy models, Alembic migrations, repository implementations
- **Queue**: Celery task definitions, Redis broker config
- **Storage**: S3/MinIO file storage adapter
- **External**: YouTube API client, TTS client, LLM client

### API Layer (`backend/api/`)
- **Routes**: `auth`, `projects`, `scripts`, `videos`, `publishing`
- **Middleware**: Auth, rate-limit, error handler, CORS
- **Dependencies**: FastAPI `Depends()` for DI

### AI Layer (`backend/ai/`)
- **Models**: LLM wrappers, embedding models
- **Prompts**: Template registry, version control
- **Pipeline**: Chain-of-thought, multi-step generation
- **Evaluation**: Quality scoring, A/B testing

### Media Layer (`backend/media/`)
- **Video**: Composition, transitions, overlays, trimming
- **Audio**: TTS generation, mixing, silence removal
- **Subtitles**: Whisper transcription, SRT/ASS generation, burn-in
- **Thumbnail**: Frame extraction, overlay text, AI generation

### Worker Layer (`backend/worker/`)
- **Tasks**: Celery tasks for long-running operations
- **Handlers**: Callbacks, webhooks, status updates

---

## 🔄 Data Flow (End-to-End)

```
User (Frontend)
  │
  ├─ 1. Create Project → POST /api/projects
  ├─ 2. Generate Script → POST /api/projects/{id}/scripts
  │     └─ AI Pipeline (LLM) → Script returned
  ├─ 3. Approve Script → PATCH /api/scripts/{id}/approve
  ├─ 4. Generate Video → POST /api/projects/{id}/generate
  │     ├─ TTS Audio Generation
  │     ├─ Video Assembly (FFmpeg)
  │     ├─ Caption Burn-in
  │     └─ Thumbnail Generation
  │     └─ (All async via Celery)
  ├─ 5. Preview → GET /api/videos/{id}/preview
  └─ 6. Publish → POST /api/videos/{id}/publish
        └─ YouTube API Upload
```

---

## 🧪 Testing Strategy

| Layer | Tool | Focus |
|-------|------|-------|
| Unit (domain) | pytest | Entities, value objects, enums |
| Unit (application) | pytest + mock | Use cases, services |
| Integration | pytest + test DB | Repositories, API routes |
| E2E | Playwright | Frontend flows |
| AI | pytest + recorded responses | Prompt outputs, quality |

---

## 🚀 Deployment

- **Dev**: `docker compose up` (API + DB + Redis + MinIO + Worker)
- **Staging**: Single VM with Docker Compose
- **Production**: Kubernetes (k8s) or AWS ECS

---

## 📦 Key Dependencies (Not Yet Installed)

### Backend (Python)
```
fastapi, uvicorn, pydantic, sqlalchemy, alembic,
celery, redis, httpx, boto3, langchain, openai,
anthropic, moviepy, pillow, pydub, whisper,
python-multipart, python-jose, passlib, sentry-sdk
```

### Frontend (Node)
```
react, react-dom, react-router-dom, zustand,
tailwindcss, vite, typescript, axios,
@tanstack/react-query, react-hook-form, zod