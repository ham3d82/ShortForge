# ShortForge 🎬

**AI-Powered YouTube Shorts Generator**

ShortForge is a production-grade application that leverages artificial intelligence to automate the creation, editing, and publishing of YouTube Shorts. Built with clean architecture principles, it separates concerns across domain logic, application services, infrastructure, and AI/Media pipelines.

---

## 📁 Project Structure (High-Level)

```
ShortForge/
├── .github/            # CI/CD workflows & issue templates
├── docs/               # Architecture docs, API reference, guides
├── frontend/           # React/TypeScript SPA (user dashboard)
├── backend/            # Python FastAPI backend (clean architecture)
├── shared/             # Shared types, schemas, and utilities
├── docker/             # Docker Compose & Dockerfiles
├── scripts/            # Dev/ops utility scripts
└── ...
```

See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for milestones and roadmap.  
See [AGENTS.md](./AGENTS.md) for AI agent orchestration design.

---

## 🧠 Core Capabilities

| Capability            | Description                                                      |
|----------------------|------------------------------------------------------------------|
| **Script Generation** | AI writes engaging Shorts scripts from a topic or prompt         |
| **Voiceover & TTS**   | Multi-voice, multi-language text-to-speech audio generation      |
| **Video Assembly**    | Compose clips, transitions, overlays into 9:16 portrait videos   |
| **Auto-Captioning**   | Burn-in subtitles with word-level timing (SRT/ASS support)       |
| **Thumbnail Creation**| AI-generated thumbnails from video content                       |
| **Schedule & Publish**| Queue, review, and push to YouTube API                           |

---

## 🏗 Architecture Overview

ShortForge follows **Clean Architecture** (Robert C. Martin) with a **Domain-Driven Design** flavor:

```
┌─────────────────────────────────────────────────────┐
│                     Frontend                         │
│            (React + TypeScript SPA)                  │
├─────────────────────────────────────────────────────┤
│                  API Layer (FastAPI)                 │
│              Routes → Middleware → Dependencies      │
├─────────────────┬───────────────────┬───────────────┤
│   Application   │     Domain        │ Infrastructure │
│   Services      │   Entities        │ DB Models      │
│   Use Cases     │   Value Objects   │ Repositories   │
│   Interfaces    │   Enums           │ Queue          │
│   DTOs          │                   │ Storage        │
├─────────────────┴───────────────────┴───────────────┤
│             AI / Media / Worker Layers              │
│   LLM Pipeline  │  Video Processing  │  Async Tasks  │
└─────────────────────────────────────────────────────┘
```

- **Frontend**: React with TypeScript, Zustand (state), React Router, Tailwind CSS
- **Backend**: Python FastAPI, SQLAlchemy 2.0, Celery (async tasks), FFmpeg
- **AI**: LangChain / OpenAI / Anthropic for script generation & prompt engineering
- **Media**: MoviePy / FFmpeg for video processing, PyDub for audio
- **Worker**: Celery workers for long-running generation tasks

---

## 🚀 Getting Started (Prerequisites)

- Python 3.11+
- Node.js 20+
- FFmpeg installed (system PATH)
- PostgreSQL 16
- Redis (for Celery)
- YouTube Data API credentials

> **Note**: Packages are not yet installed. See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for setup instructions.

---

## 🔧 Tech Stack

| Layer         | Technology                                        |
|---------------|---------------------------------------------------|
| Frontend      | React 19, TypeScript, Vite, Zustand, Tailwind     |
| Backend       | Python 3.11+, FastAPI, Pydantic V2, SQLAlchemy 2.0|
| Async Tasks   | Celery + Redis                                    |
| AI / LLM      | LangChain, OpenAI, Anthropic, HuggingFace         |
| Media         | FFmpeg, MoviePy, Pillow, PyDub, Whisper           |
| Database      | PostgreSQL 16                                     |
| Storage       | AWS S3 / MinIO (local dev)                        |
| Container     | Docker + Docker Compose                           |
| CI/CD         | GitHub Actions                                    |

---

## 📄 License

MIT — See [LICENSE](LICENSE) for details.