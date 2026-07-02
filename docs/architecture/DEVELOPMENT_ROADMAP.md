# ShortForge — Development Roadmap

> **Author**: Principal Software Architect  
> **Version**: 1.0.0  
> **Last Updated**: 2026-07-02

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Phase Breakdown](#2-phase-breakdown)
3. [Dependency Graph](#3-dependency-graph)
4. [Team Structure](#4-team-structure)
5. [Milestone Deliverables](#5-milestone-deliverables)
6. [Risk Assessment](#6-risk-assessment)
7. [Success Metrics](#7-success-metrics)

---

## 1. Executive Summary

### Vision
Build a production-grade, AI-powered YouTube Shorts generator in **16 weeks** across **7 phases**, with a team of **5-8 engineers**.

### Key Milestones

| Milestone | Week | Deliverable |
|-----------|------|-------------|
| **M1: Foundation** | 2 | Running Docker stack, health check, DB migrations |
| **M2: Auth & Users** | 4 | User registration, JWT auth, YouTube OAuth2 |
| **M3: Script Generation** | 6 | AI script generation with prompt registry |
| **M4: Media Pipeline** | 9 | TTS, image gen, video composition, captions |
| **M5: YouTube Publishing** | 11 | Upload, schedule, publish to YouTube |
| **M6: Frontend Dashboard** | 14 | Full UI: projects, generation wizard, preview |
| **M7: Production Hardening** | 16 | Monitoring, caching, load testing, docs |

### Resource Requirements

| Resource | Phase 1-2 | Phase 3-4 | Phase 5-7 |
|----------|-----------|-----------|-----------|
| **Backend Engineers** | 2 | 3 | 2 |
| **Frontend Engineers** | 1 | 2 | 2 |
| **AI/ML Engineers** | 0 | 2 | 1 |
| **DevOps** | 1 (shared) | 1 | 1 |
| **GPU (RTX 4090)** | 0 | 2 | 2 |
| **Total Team** | 4 | 8 | 6 |

---

## 2. Phase Breakdown

### Phase 1: Foundation (Weeks 1-2)

**Objective**: Establish the development environment, project structure, and core infrastructure.

#### Week 1: Project Scaffolding

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Initialize Python project with Poetry | Backend | 4h | None |
| Initialize React project with Vite | Frontend | 4h | None |
| Set up Docker Compose (API, DB, Redis, MinIO) | DevOps | 8h | None |
| Configure ESLint, Prettier, mypy, ruff | Backend | 4h | Project init |
| Create FastAPI app skeleton with health check | Backend | 4h | Docker |
| Set up SQLAlchemy + Alembic | Backend | 6h | Docker |
| Create initial migration (users table) | Backend | 4h | Alembic |
| Configure CI/CD (GitHub Actions) | DevOps | 8h | Docker |

**Deliverables**: Running `docker compose up` with API at `localhost:8000/docs`

#### Week 2: Core Infrastructure

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Implement config management (Pydantic Settings) | Backend | 4h | Week 1 |
| Set up logging (structlog) | Backend | 3h | Config |
| Implement error handling middleware | Backend | 4h | FastAPI |
| Set up Redis connection + health check | Backend | 3h | Docker |
| Set up MinIO/S3 storage adapter | Backend | 6h | Docker |
| Create Celery app + Redis broker | Backend | 6h | Redis |
| Create Celery Beat schedule | Backend | 3h | Celery |
| Set up Flower monitoring | DevOps | 2h | Celery |
| Create base repository pattern | Backend | 4h | SQLAlchemy |
| Write unit test framework + first tests | Backend | 4h | Project init |

**Deliverables**: All infrastructure services running, health checks passing, CI pipeline green

**Phase 1 Total**: ~60 hours engineering time

---

### Phase 2: User & Auth (Weeks 3-4)

**Objective**: Implement user management, authentication, and YouTube OAuth2 integration.

#### Week 3: User Management

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create User domain entity + value objects | Backend | 4h | Phase 1 |
| Implement UserRepository | Backend | 3h | Repository pattern |
| Create user registration endpoint | Backend | 4h | User entity |
| Implement password hashing (bcrypt) | Backend | 2h | Security |
| Create login endpoint + JWT issuance | Backend | 6h | User repo |
| Implement refresh token flow | Backend | 4h | JWT |
| Create logout + token blacklist | Backend | 3h | Redis |
| Write auth middleware | Backend | 4h | JWT |
| Create user profile endpoints | Backend | 3h | Auth |
| Write integration tests for auth | Backend | 4h | Auth endpoints |

**Deliverables**: Full auth flow working (register → login → access resources)

#### Week 4: YouTube OAuth2 & Rate Limiting

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create YouTube account entity | Backend | 3h | User entity |
| Implement YouTube OAuth2 flow | Backend | 8h | Google API |
| Create YouTube API client (upload) | Backend | 6h | OAuth2 |
| Implement rate limiting middleware | Backend | 4h | Redis |
| Create admin endpoints (user management) | Backend | 4h | Auth |
| Implement role-based access control | Backend | 4h | Auth |
| Add request ID tracing middleware | Backend | 2h | Phase 1 |
| Write E2E tests for auth flow | Backend | 4h | Auth |
| Frontend: Login/Register pages | Frontend | 8h | Auth API |
| Frontend: Auth context + protected routes | Frontend | 6h | Login page |

**Deliverables**: User can register, login, connect YouTube account

**Phase 2 Total**: ~80 hours engineering time

---

### Phase 3: AI Script Generation (Weeks 5-6)

**Objective**: Implement the AI-powered script generation pipeline with prompt management.

#### Week 5: LLM Integration

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create IAIService port interface | Backend | 3h | Phase 1 |
| Implement OpenAI adapter | Backend | 6h | IAIService |
| Implement Anthropic adapter | Backend | 4h | IAIService |
| Implement Ollama adapter (local) | Backend | 4h | IAIService |
| Create ProviderRegistry | Backend | 4h | Adapters |
| Implement circuit breaker for providers | Backend | 4h | Registry |
| Create PromptRegistry with versioning | Backend | 6h | Phase 1 |
| Write prompt templates (hook, body, CTA) | AI/ML | 8h | Prompt registry |
| Create content safety filter | Backend | 4h | Phase 1 |
| Write unit tests for LLM adapters | Backend | 4h | Adapters |

**Deliverables**: Can call any LLM provider through unified interface

#### Week 6: Script Generation Pipeline

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create Project entity + repository | Backend | 4h | Phase 1 |
| Create Script entity + repository | Backend | 4h | Phase 1 |
| Implement GenerateScript use case | Backend | 8h | LLM adapters |
| Implement topic analysis step | AI/ML | 6h | LLM |
| Implement hook generation step | AI/ML | 4h | LLM |
| Implement body structure step | AI/ML | 6h | LLM |
| Implement CTA generation step | AI/ML | 3h | LLM |
| Implement scene parsing + validation | Backend | 6h | Script entity |
| Implement script quality evaluation | AI/ML | 8h | LLM |
| Create script CRUD endpoints | Backend | 6h | Use cases |
| Implement script approval flow | Backend | 4h | Script endpoints |
| Write integration tests for script pipeline | Backend | 6h | All above |

**Deliverables**: User can create project → generate script → approve

**Phase 3 Total**: ~100 hours engineering time

---

### Phase 4: Media Pipeline (Weeks 7-9)

**Objective**: Implement TTS, image generation, video composition, and captioning.

#### Week 7: Audio Pipeline

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create ITTSProvider port | Backend | 3h | Phase 1 |
| Implement ElevenLabs adapter | Backend | 6h | ITTSProvider |
| Implement Azure TTS adapter | Backend | 4h | ITTSProvider |
| Implement local TTS fallback (pyttsx3) | Backend | 3h | ITTSProvider |
| Create Voiceover entity + repository | Backend | 4h | Phase 1 |
| Implement GenerateTTS use case | Backend | 6h | TTS adapters |
| Implement silence insertion | Backend | 4h | Audio |
| Implement audio mixer (voiceover + BGM) | Backend | 8h | Audio |
| Create audio endpoints | Backend | 4h | Use cases |
| Write tests for audio pipeline | Backend | 4h | All above |

**Deliverables**: Script → TTS audio with proper pacing and mixing

#### Week 8: Image Pipeline

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create IImageProvider port | Backend | 3h | Phase 1 |
| Implement Stability AI adapter | Backend | 6h | IImageProvider |
| Implement FLUX adapter | Backend | 4h | IImageProvider |
| Implement local SD adapter | Backend | 6h | IImageProvider |
| Create Image entity + repository | Backend | 4h | Phase 1 |
| Implement GenerateImage use case | Backend | 6h | Image adapters |
| Implement prompt expansion for images | AI/ML | 6h | LLM |
| Implement image upscaling (Real-ESRGAN) | Backend | 8h | GPU |
| Implement Ken Burns effect | Backend | 6h | FFmpeg |
| Implement Deforum animation | AI/ML | 12h | GPU |
| Create image endpoints | Backend | 4h | Use cases |
| Write tests for image pipeline | Backend | 4h | All above |

**Deliverables**: Scene descriptions → generated, upscaled, animated images

#### Week 9: Video Composition & Captions

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create IVideoPipeline port | Backend | 3h | Phase 1 |
| Implement ScenePlanner | Backend | 8h | Script + images |
| Implement CompositionGraphBuilder | Backend | 8h | FFmpeg |
| Implement FFmpeg CLI generator | Backend | 6h | FFmpeg |
| Implement render progress monitor | Backend | 4h | FFmpeg |
| Implement pre-flight validator | Backend | 4h | All assets |
| Create Video entity + repository | Backend | 4h | Phase 1 |
| Implement Whisper transcription | Backend | 8h | GPU |
| Implement SRT/ASS formatter | Backend | 6h | Whisper |
| Implement caption burn-in (ASS filter) | Backend | 6h | FFmpeg |
| Implement thumbnail generation | Backend | 4h | FFmpeg |
| Create video endpoints | Backend | 6h | Use cases |
| Implement quality tier fallback | Backend | 4h | All pipelines |
| Write integration tests for full pipeline | Backend | 8h | All above |

**Deliverables**: Full end-to-end: script → audio → images → captions → video

**Phase 4 Total**: ~180 hours engineering time

---

### Phase 5: YouTube Publishing (Weeks 10-11)

**Objective**: Implement YouTube API integration for uploading, scheduling, and publishing.

#### Week 10: YouTube Integration

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Create IPublishService port | Backend | 3h | Phase 1 |
| Implement YouTube upload client | Backend | 8h | YouTube API |
| Implement resumable upload protocol | Backend | 6h | YouTube client |
| Create Publication entity + repository | Backend | 4h | Phase 1 |
| Implement PublishToYouTube use case | Backend | 6h | YouTube client |
| Implement scheduled publishing | Backend | 4h | Celery Beat |
| Implement publish retry with backoff | Backend | 4h | Celery |
| Create publishing endpoints | Backend | 4h | Use cases |
| Write tests for YouTube client (mocked) | Backend | 6h | All above |

**Deliverables**: Can upload video to YouTube with metadata

#### Week 11: Publishing Dashboard

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Implement publish status tracking | Backend | 4h | Week 10 |
| Implement publish history | Backend | 3h | Week 10 |
| Implement cancel scheduled publish | Backend | 3h | Week 10 |
| Create WebSocket for real-time updates | Backend | 6h | Phase 1 |
| Frontend: YouTube account connection UI | Frontend | 6h | OAuth2 |
| Frontend: Publish dialog (title, desc, tags) | Frontend | 8h | Publishing API |
| Frontend: Publishing queue view | Frontend | 6h | Publishing API |
| Frontend: Publish history + status | Frontend | 4h | Publishing API |
| Write E2E tests for publish flow | QA | 8h | All above |

**Deliverables**: Full publish flow: preview → configure → schedule/publish → track

**Phase 5 Total**: ~100 hours engineering time

---

### Phase 6: Frontend Dashboard (Weeks 12-14)

**Objective**: Build the complete user-facing React application.

#### Week 12: Core UI

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Set up React Router + layout | Frontend | 4h | Phase 1 |
| Create design system (Tailwind components) | Frontend | 8h | Phase 1 |
| Implement Zustand stores (auth, projects) | Frontend | 6h | Phase 1 |
| Create API client layer (axios) | Frontend | 4h | Phase 1 |
| Build project list page | Frontend | 6h | API |
| Build project creation form | Frontend | 6h | API |
| Build project detail page | Frontend | 8h | API |
| Implement project CRUD operations | Frontend | 6h | API |
| Add loading states + error handling | Frontend | 4h | All pages |

**Deliverables**: User can create, view, edit, delete projects

#### Week 13: Generation Wizard

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Build multi-step generation wizard | Frontend | 12h | Project UI |
| Step 1: Topic + settings form | Frontend | 4h | Wizard |
| Step 2: Script preview + hook selection | Frontend | 8h | Script API |
| Step 3: Script editor (manual edit) | Frontend | 6h | Script API |
| Step 4: Audio preview + voice selection | Frontend | 6h | Audio API |
| Step 5: Image gallery + scene view | Frontend | 8h | Image API |
| Step 6: Caption style editor | Frontend | 4h | Caption API |
| Step 7: Video preview player | Frontend | 8h | Video API |
| Implement generation progress tracking | Frontend | 6h | WebSocket |
| Implement WebSocket connection manager | Frontend | 4h | Phase 1 |

**Deliverables**: Full generation wizard with real-time progress

#### Week 14: Polish & Advanced Features

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Build video preview player (custom) | Frontend | 8h | Video API |
| Implement dark mode | Frontend | 4h | Design system |
| Add responsive design (mobile) | Frontend | 8h | All pages |
| Implement project duplication | Frontend | 3h | Project API |
| Add keyboard shortcuts | Frontend | 3h | Wizard |
| Implement undo/redo for script editor | Frontend | 6h | Script editor |
| Add tour/onboarding for new users | Frontend | 6h | All features |
| Performance optimization (lazy loading) | Frontend | 4h | All pages |
| Write Playwright E2E tests | QA | 12h | All pages |
| Accessibility audit + fixes | Frontend | 6h | All pages |

**Deliverables**: Polished, responsive, accessible frontend application

**Phase 6 Total**: ~180 hours engineering time

---

### Phase 7: Production Hardening (Weeks 15-16)

**Objective**: Production-ready monitoring, performance optimization, and documentation.

#### Week 15: Monitoring & Performance

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Set up Prometheus metrics | DevOps | 6h | Phase 1 |
| Set up Grafana dashboards | DevOps | 8h | Prometheus |
| Implement Sentry error tracking | Backend | 4h | Phase 1 |
| Set up OpenTelemetry tracing | Backend | 8h | Phase 1 |
| Implement AI response caching (Redis) | Backend | 6h | Phase 1 |
| Implement database query optimization | Backend | 8h | Phase 1 |
| Add database connection pooling tuning | Backend | 4h | Phase 1 |
| Implement CDN caching for media | DevOps | 4h | S3 |
| Load testing (locust) | QA | 12h | All APIs |
| Performance profiling + optimization | Backend | 8h | All |

**Deliverables**: Monitoring dashboards, performance baselines, caching

#### Week 16: Documentation & Deployment

| Task | Owner | Effort | Dependencies |
|------|-------|--------|--------------|
| Write API documentation (OpenAPI) | Backend | 6h | All APIs |
| Write deployment guide | DevOps | 8h | Docker |
| Write developer setup guide | Backend | 4h | Phase 1 |
| Create Kubernetes manifests | DevOps | 12h | Docker |
| Set up staging environment | DevOps | 8h | K8s |
| Implement backup strategy | DevOps | 6h | DB |
| Security audit + fixes | Backend | 8h | All |
| Final integration tests | QA | 12h | All |
| Bug bash + triage | All | 8h | All |
| Production deployment runbook | DevOps | 6h | All |

**Deliverables**: Production-ready deployment, comprehensive documentation

**Phase 7 Total**: ~140 hours engineering time

---

## 3. Dependency Graph

```
Phase 1: Foundation
  │
  ├──► Phase 2: Auth & Users
  │      │
  │      ├──► Phase 3: AI Script Gen
  │      │      │
  │      │      └──► Phase 4: Media Pipeline
  │      │             │
  │      │             └──► Phase 5: YouTube Publishing
  │      │                    │
  │      └────────────────────┼──► Phase 6: Frontend Dashboard
  │                           │
  └───────────────────────────┴──► Phase 7: Production Hardening
```

**Parallelization Opportunities**:
- Phase 3 (Script) and Phase 4 (Media) can overlap by 1 week
- Phase 5 (Publishing) can start once Phase 4 video output is stable
- Phase 6 (Frontend) can start in Week 8 (parallel with Phase 4)
- Phase 7 (Hardening) is sequential (needs all features)

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 7  
**Total critical path**: 16 weeks

---

## 4. Team Structure

### Recommended Team Composition

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Engineering Team                                                        │
│                                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐                       │
│  │  Backend Team (3)   │  │  Frontend Team (2)  │                       │
│  │                     │  │                      │                       │
│  │  BE-1: API + Auth   │  │  FE-1: Core UI +    │                       │
│  │        + Infra      │  │        Dashboard     │                       │
│  │                     │  │                      │                       │
│  │  BE-2: AI + Media   │  │  FE-2: Wizard +     │                       │
│  │        + Pipeline   │  │        Preview       │                       │
│  │                     │  │                      │                       │
│  │  BE-3: YouTube +    │  │                      │                       │
│  │        Workers      │  │                      │                       │
│  └─────────────────────┘  └─────────────────────┘                       │
│                                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐                       │
│  │  AI/ML Team (1-2)   │  │  DevOps (1)         │                       │
│  │                     │  │                      │                       │
│  │  ML-1: Prompt Eng   │  │  D-1: Docker + K8s  │                       │
│  │        + Evaluation │  │        + CI/CD       │                       │
│  │                     │  │                      │                       │
│  │  ML-2: Image Gen    │  │                      │                       │
│  │        + Animation  │  │                      │                       │
│  └─────────────────────┘  └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Role Responsibilities

| Role | Primary | Secondary |
|------|---------|-----------|
| **BE-1** | API design, auth, infrastructure, DB | Code review, architecture |
| **BE-2** | AI pipeline, media processing, FFmpeg | Performance optimization |
| **BE-3** | YouTube API, Celery workers, WebSocket | Error handling, monitoring |
| **FE-1** | Design system, project CRUD, auth UI | Accessibility, responsive |
| **FE-2** | Generation wizard, video preview, WebSocket | State management, perf |
| **ML-1** | Prompt engineering, quality evaluation | LLM provider management |
| **ML-2** | Image generation, animation, upscaling | GPU optimization |
| **DevOps** | Docker, CI/CD, monitoring, deployment | Security, backup |

---

## 5. Milestone Deliverables

### M1: Foundation (Week 2)

```
✅ Docker Compose running all services
✅ FastAPI health check at /api/v1/health
✅ PostgreSQL with Alembic migrations
✅ Redis connected and responsive
✅ MinIO/S3 storage accessible
✅ Celery worker processing tasks
✅ Flower monitoring dashboard
✅ GitHub Actions CI passing
✅ Logging and error handling
✅ Base repository pattern implemented
```

### M2: Auth & Users (Week 4)

```
✅ User registration (POST /auth/register)
✅ User login (POST /auth/login)
✅ JWT access + refresh tokens
✅ Token refresh flow
✅ Logout with token blacklist
✅ YouTube OAuth2 connection
✅ Rate limiting (100 req/min)
✅ Role-based access (creator, premium, admin)
✅ Admin user management endpoints
✅ Frontend: Login/Register pages
✅ Frontend: Protected routes
```

### M3: Script Generation (Week 6)

```
✅ LLM provider abstraction (OpenAI, Anthropic, Ollama)
✅ Provider registry with circuit breaker
✅ Prompt registry with versioning
✅ Topic analysis prompt
✅ Hook generation (3 options)
✅ Body structure with scene breakdown
✅ CTA generation (3 options)
✅ Scene parsing and validation
✅ Script quality evaluation
✅ Script CRUD endpoints
✅ Script approval flow
```

### M4: Media Pipeline (Week 9)

```
✅ TTS generation (ElevenLabs, Azure, local)
✅ Audio mixing (voiceover + BGM)
✅ Silence insertion for pacing
✅ Image generation (Stability, FLUX, local SD)
✅ Image upscaling (Real-ESRGAN)
✅ Ken Burns effect on images
✅ Deforum animation (optional)
✅ Whisper transcription
✅ SRT/ASS caption generation
✅ Word-by-word highlight captions
✅ Caption burn-in (ASS filter)
✅ Video composition engine
✅ FFmpeg GPU acceleration (NVENC)
✅ Scene planning and layout
✅ Thumbnail generation
✅ Quality tier fallback (draft/standard/high)
```

### M5: YouTube Publishing (Week 11)

```
✅ YouTube OAuth2 token management
✅ Resumable video upload
✅ Video metadata (title, description, tags)
✅ Scheduled publishing
✅ Publish retry with exponential backoff
✅ Publish status tracking
✅ Publish history
✅ Cancel scheduled publish
✅ WebSocket real-time updates
✅ Frontend: Publish dialog
✅ Frontend: Publishing queue
```

### M6: Frontend Dashboard (Week 14)

```
✅ Project list with pagination
✅ Project creation form
✅ Project detail view
✅ Multi-step generation wizard
✅ Script preview + hook selection
✅ Script editor (manual edit)
✅ Audio preview + voice selection
✅ Image gallery + scene view
✅ Caption style editor
✅ Video preview player
✅ Generation progress tracking
✅ Dark mode
✅ Responsive design (mobile)
✅ Keyboard shortcuts
✅ Onboarding tour
✅ E2E tests (Playwright)
```

### M7: Production Hardening (Week 16)

```
✅ Prometheus metrics
✅ Grafana dashboards
✅ Sentry error tracking
✅ OpenTelemetry tracing
✅ AI response caching (Redis)
✅ Database query optimization
✅ CDN caching for media
✅ Load testing results (1000 concurrent users)
✅ Performance optimization (p95 < 200ms)
✅ Kubernetes manifests
✅ Staging environment
✅ Backup strategy implemented
✅ Security audit completed
✅ Deployment runbook
✅ Developer setup guide
✅ API documentation
```

---

## 6. Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **LLM API rate limits** | High | Medium | Provider abstraction with automatic failover; local Ollama fallback |
| **GPU availability** | Medium | High | CPU fallback for all GPU operations; quality degradation instead of failure |
| **FFmpeg compatibility** | Medium | Medium | Extensive version testing in CI; pin FFmpeg version in Docker |
| **YouTube API changes** | Low | High | Abstract YouTube client behind interface; monitor API changelog |
| **Whisper accuracy** | Medium | Medium | Script alignment post-processing; manual caption editing option |
| **Image generation quality** | Medium | Medium | Multiple providers; quality evaluation; user can regenerate |
| **Database performance** | Low | High | Connection pooling; query optimization; read replicas in Phase 7 |
| **Memory leaks in workers** | Medium | Medium | Worker restart after N jobs; memory monitoring in Grafana |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **AI pipeline complexity** | High | Medium | Start with simple pipeline in Phase 3, iterate in Phase 4 |
| **GPU procurement delay** | Medium | High | Use cloud GPU (RunPod, Lambda) while waiting for hardware |
| **YouTube API quota limits** | Medium | Medium | Implement quota tracking; user-facing quota display |
| **Frontend scope creep** | Medium | Medium | MVP features only in Phase 6; advanced features post-launch |
| **Integration complexity** | High | Medium | Weekly integration demos; catch issues early |

### Mitigation Budget

| Item | Hours | Cost |
|------|-------|------|
| **Buffer time** (15% of total) | ~120h | Included in estimates |
| **Spike research** (new tech) | 40h | Week 1-2 |
| **Bug fixing** | 80h | Throughout |
| **Code review** | 60h | Throughout |
| **Documentation** | 40h | Phase 7 |

---

## 7. Success Metrics

### Technical KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| **API Response Time (p95)** | < 200ms | Prometheus |
| **Script Generation Time** | < 10s | Application metrics |
| **Video Render Time (30s Short)** | < 30s (GPU) | Application metrics |
| **Full Pipeline (60s video)** | < 5 min | Application metrics |
| **System Uptime** | 99.9% | Uptime monitoring |
| **Error Rate (5xx)** | < 0.1% | Prometheus |
| **Test Coverage** | > 85% | pytest-cov |
| **Build Time** | < 10 min | GitHub Actions |

### Business KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Videos Generated per Day** | 1000+ | Database |
| **Average Generation Time** | < 3 min | Application metrics |
| **User Retention (Day 7)** | > 40% | Analytics |
| **Script Approval Rate** | > 80% | Database |
| **Publish Success Rate** | > 95% | Database |
| **User Satisfaction (NPS)** | > 50 | Survey |

### Quality Gates

| Gate | Criteria | Phase |
|------|----------|-------|
| **Code Review** | 2 approvals, no unresolved comments | All |
| **Test Coverage** | > 80% for new code | All |
| **Integration Tests** | All critical paths pass | All |
| **Performance** | No regression > 10% | Phase 7 |
| **Security** | No critical/high vulnerabilities | Phase 7 |
| **Accessibility** | WCAG 2.1 AA compliance | Phase 6 |
| **Documentation** | All endpoints documented | Phase 7 |

---

## Appendix: Effort Summary

| Phase | Weeks | Backend | Frontend | AI/ML | DevOps | Total Hours |
|-------|-------|---------|----------|-------|--------|-------------|
| **1: Foundation** | 2 | 40h | 8h | 0h | 12h | **60h** |
| **2: Auth & Users** | 2 | 52h | 14h | 0h | 0h | **66h** |
| **3: Script Gen** | 2 | 56h | 0h | 35h | 0h | **91h** |
| **4: Media Pipeline** | 3 | 100h | 0h | 18h | 0h | **118h** |
| **5: YouTube Pub** | 2 | 48h | 24h | 0h | 0h | **72h** |
| **6: Frontend** | 3 | 0h | 140h | 0h | 0h | **140h** |
| **7: Hardening** | 2 | 38h | 0h | 0h | 44h | **82h** |
| **Buffer** | - | 30h | 20h | 10h | 10h | **70h** |
| **Total** | **16** | **364h** | **206h** | **63h** | **66h** | **~700h** |

### Team Loading

```
Week:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
BE-1:  ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██
BE-2:  ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██
BE-3:  ░░ ░░ ░░ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██
FE-1:  ██ ██ ██ ██ ░░ ░░ ░░ ██ ██ ██ ██ ██ ██ ██ ██ ██
FE-2:  ░░ ░░ ░░ ██ ░░ ░░ ░░ ██ ██ ██ ██ ██ ██ ██ ██ ██
ML-1:  ░░ ░░ ░░ ░░ ██ ██ ██ ██ ██ ░░ ░░ ░░ ░░ ░░ ░░ ░░
ML-2:  ░░ ░░ ░░ ░░ ░░ ░░ ░░ ██ ██ ░░ ░░ ░░ ░░ ░░ ░░ ░░
DevOps:██ ██ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ██ ██

██ = Full time  ██ = Part time  ░░ = Not needed
```

---

## Appendix B: Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/your-org/shortforge.git
cd shortforge

# Backend setup
cd backend
poetry install
poetry run alembic upgrade head
poetry run uvicorn main:app --reload

# Frontend setup
cd frontend
npm install
npm run dev

# Docker (full stack)
cd docker
docker compose up -d

# Run tests
cd backend && poetry run pytest
cd frontend && npm test

# Run workers
cd backend
poetry run celery -A worker.celery_app worker -l info
poetry run celery -A worker.celery_app beat -l info