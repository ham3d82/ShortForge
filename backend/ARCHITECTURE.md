# ShortForge Architecture

> **Document Type:** Software Architecture Document (SAD)
>
> **Project:** ShortForge
>
> **Version:** 2.0
>
> **Status:** Active
>
> **Last Updated:** 2026-07-06

---

# 1. Executive Summary

## Purpose

This document defines the software architecture of ShortForge.

Its purpose is to document the architectural decisions, system structure, design principles, and component responsibilities that govern the project.

This document serves as the single source of truth for how the backend is designed and how future features should integrate into the system.

It is intended to evolve alongside the project while preserving architectural consistency.

---

## Intended Audience

This document is written for:

- Software Architects
- Backend Engineers
- Future Contributors
- Technical Reviewers
- Project Maintainers

It assumes familiarity with Python, FastAPI, SQLAlchemy, asynchronous programming, and modern backend design patterns.

---

## Goals

The architecture aims to achieve the following objectives:

- Maintain a clean separation of concerns.
- Keep business logic independent of frameworks.
- Isolate external AI providers behind stable interfaces.
- Allow replacing infrastructure without changing business logic.
- Support incremental feature growth without architectural rewrites.
- Keep the codebase understandable as the project scales.

---

## Scope

This document covers the backend architecture only.

Included:

- API Layer
- Dependency Injection
- Workflow Layer
- Services
- Repositories
- Database
- AI Providers
- Storage
- Application Boundaries
- Architectural Decisions

Excluded:

- Frontend implementation
- Infrastructure deployment
- CI/CD pipelines
- Monitoring
- Cost optimization
- Security hardening details

These subjects will have dedicated documents as the project grows.

---

# 2. System Vision

ShortForge is an AI-powered content generation platform capable of producing complete short-form videos from a single user request.

The long-term objective is to transform one high-level idea into a fully publishable video through a modular generation pipeline.

The system is designed around independent business capabilities that cooperate through orchestration rather than direct coupling.

Every new capability should integrate into the existing architecture with minimal modification to existing components.

---

## Current Capabilities

The current implementation supports:

- Script generation
- Project persistence
- AI provider abstraction
- Image generation
- Image persistence
- Static image serving
- End-to-end generation workflow

---

## Planned Capabilities

Future milestones include:

- Voice generation
- Subtitle generation
- Thumbnail generation
- Timeline construction
- Video rendering
- FFmpeg integration
- Asset management
- Publishing integrations
- Background job processing
- Multiple AI providers

The architecture intentionally anticipates these features without introducing unnecessary complexity today.

---

# 3. Architectural Philosophy

The architecture follows a layered, modular, service-oriented design.

Business logic must remain independent from frameworks, databases, and AI providers.

Framework code should orchestrate—not implement—business rules.

External services should be treated as replaceable dependencies rather than core components.

Every architectural decision should improve maintainability before optimizing for convenience.

---

## Core Principles

### Single Responsibility

Each component should have one clearly defined responsibility.

Examples:

- ScriptService generates scripts.
- ImageService generates images.
- ProjectRepository persists projects.

Responsibilities should never overlap.

---

### Separation of Concerns

Every layer owns a single concern.

Presentation, orchestration, business logic, persistence, and provider communication remain isolated.

Changes in one layer should have minimal impact on others.

---

### Dependency Inversion

High-level modules must not depend on implementation details.

Business services communicate through abstractions whenever possible.

External providers remain implementation details hidden behind interfaces.

---

### Composition over Inheritance

Application behavior should be assembled through composition instead of deep inheritance hierarchies.

Services collaborate through dependency injection rather than subclassing.

---

### Explicit Dependencies

Every dependency should be visible through constructor injection.

Objects should never create their own collaborators internally unless they are simple value objects.

This improves readability, testing, and maintainability.

---

### Progressive Evolution

The architecture should evolve incrementally.

The system should never be redesigned simply because a new feature is introduced.

Instead, new capabilities should extend existing architectural boundaries.

This minimizes regressions while preserving long-term stability.

---

# 4. Quality Attributes

Architecture decisions are evaluated against the following quality attributes.

## Maintainability

Maintainability is the highest priority.

Developers should understand the location and responsibility of every component without tracing unrelated code.

---

## Modularity

Business capabilities must remain isolated.

Adding Voice generation should not require modifications inside Script generation.

---

## Extensibility

Replacing Gemini with another provider should not require changes to business logic.

Adding a second image provider should require minimal modifications.

---

## Testability

Business logic should remain testable independently from FastAPI, databases, and external APIs.

Dependencies should be injectable to enable isolated testing.

---

## Scalability

The architecture should support future migration toward:

- Background workers
- Distributed execution
- Queue systems
- Object storage
- Multiple AI providers

without requiring a complete redesign.

---

## Readability

Code should prioritize clarity over cleverness.

Architecture should be understandable by new contributors after reading this document.
---
# 5. System Context

## Overview

ShortForge is designed as a layered backend application where every request flows through well-defined architectural boundaries.

The system accepts client requests through a REST API, orchestrates business operations using workflows, delegates business logic to services, persists data through repositories, and communicates with external AI providers using provider abstractions.

No layer should bypass another layer.

Each layer has explicit responsibilities and controlled dependencies.

---

## External Systems

The current implementation communicates with the following external systems.

### AI Providers

Responsible for generating content.

Current providers:

- Gemini (Text)
- Pollinations (Images)
- Gemini (Images)

Future providers:

- OpenAI
- OpenRouter
- Stability AI
- Flux
- Other compatible providers

Providers are considered infrastructure components.

Business logic must never depend on provider-specific implementations.

---

### Database

Current database:

- PostgreSQL

Responsibilities:

- Persist projects
- Persist generated images
- Store future media metadata

The database is accessed exclusively through repositories.

---

### File Storage

Generated images are stored locally.

Responsibilities:

- Persist generated media
- Expose static files through FastAPI

Future versions may replace local storage with:

- Amazon S3
- Cloudflare R2
- Azure Blob Storage
- Google Cloud Storage

The storage mechanism should remain transparent to business services.

---

### Clients

Current clients:

- Swagger UI
- REST Clients
- Frontend (future)

Clients communicate only through HTTP endpoints.

They never access business logic directly.

---

# 6. High-Level Architecture

The backend follows a layered architecture.

```

```text
                Client
                   │
                   ▼
              FastAPI API
                   │
                   ▼
          Dependency Injection
                   │
                   ▼
          Workflow Layer
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
 ScriptService ImageService ProjectService
        │          │
        └──────┬───┘
               ▼
           AIService
        ┌──────┴────────┐
        ▼               ▼
 Text Provider     Image Provider
        │               │
   Gemini/OpenAI   Pollinations/Gemini

Repositories
        │
        ▼
 PostgreSQL
```

---

## Architectural Layers

The architecture is divided into independent layers.

Each layer has one responsibility and communicates only with adjacent layers.

```

```text
API
 ↓

Dependencies
 ↓

Workflows
 ↓

Services
 ↓

Repositories
 ↓

Database
```

---

### API Layer

Responsible for:

- Receiving HTTP requests
- Request validation
- Response serialization
- Dependency resolution

The API layer must never contain business logic.

---

### Dependency Layer

Responsible for constructing application objects.

Examples:

- AIService
- ScriptService
- ImageService
- GenerationWorkflow

Dependencies centralize object creation and wiring.

Business objects should never instantiate their collaborators directly.

---

### Workflow Layer

Responsible for orchestration.

A workflow coordinates multiple services to accomplish a business process.

Example:

Generate Project

↓

Generate Script

↓

Save Project

↓

Generate Images

↓

Save Images

↓

Return Response

Workflows coordinate business operations but do not implement business rules.

---

### Service Layer

Responsible for business logic.

Every service represents one business capability.

Current services include:

- AIService
- ScriptService
- ImageService
- ProjectService
- GeneratedImageService

Services may collaborate with other services when appropriate but should avoid unnecessary coupling.

---

### Repository Layer

Responsible exclusively for persistence.

Repositories translate business operations into database operations.

Responsibilities include:

- Create
- Read
- Update
- Delete

Repositories must never contain business rules.

---

### Infrastructure Layer

Infrastructure components communicate with external systems.

Examples:

- AI Providers
- Database Driver
- Local Storage
- Future Cloud Storage

Infrastructure implementations remain replaceable.

Business logic must remain independent from infrastructure decisions.

---

# 7. Dependency Rules

The architecture enforces strict dependency boundaries.

Allowed dependency direction:

```

```text
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

Forbidden examples:

✗ Repository calling Service

✗ Provider calling Repository

✗ API accessing Database directly

✗ Workflow querying Database directly

✗ Provider importing FastAPI

✗ Repository communicating with AI providers

---

## Dependency Injection

All application services should receive collaborators through constructor injection.

Correct:

```

```python
class ScriptService:

    def __init__(
        self,
        ai: AIService,
        project_service: ProjectService,
    ):
        ...
```

Avoid creating dependencies internally:

```

```python
# Avoid

class ScriptService:

    def __init__(self):

        self.ai = AIService(...)
```

Centralized dependency injection improves:

- Testability
- Readability
- Replaceability
- Configuration management

---

## Circular Dependencies

Circular dependencies are prohibited.

If two services require each other, the architecture should be redesigned.

Typical solutions include:

- Introducing a Workflow
- Extracting shared logic
- Introducing a new service
- Moving orchestration upward

Circular dependencies are considered architectural violations.
---

# 8. Request Lifecycle

Every request follows the same architectural lifecycle regardless of the feature being executed.

The objective is to ensure a predictable execution path throughout the application.

```

```text
HTTP Request

↓

API Route

↓

Request Validation

↓

Dependency Resolution

↓

Workflow

↓

Business Services

↓

Repositories

↓

Database / AI Providers

↓

Response Mapping

↓

HTTP Response
```

---

## Step 1 — API Route

The request enters the application through a FastAPI endpoint.

Responsibilities:

- Receive the HTTP request.
- Validate input schemas.
- Resolve dependencies.
- Delegate execution.

The route must never contain business logic.

---

## Step 2 — Dependency Resolution

FastAPI resolves all required application objects.

Examples include:

- AIService
- ScriptService
- ImageService
- GenerationWorkflow

Object creation is centralized inside the dependency layer.

---

## Step 3 — Workflow Execution

The workflow represents the business process.

Example:

Project Generation

↓

Generate Script

↓

Persist Project

↓

Generate Images

↓

Persist Images

↓

Return Complete Response

The workflow coordinates services but never implements domain rules.

---

## Step 4 — Business Services

Each service performs one business capability.

Examples:

ScriptService

- builds prompts
- requests AI generation
- validates structured responses
- persists project

ImageService

- loads project
- generates images
- stores generated files
- persists image metadata

ProjectService

- project lifecycle management

GeneratedImageService

- generated image lifecycle management

Services are reusable across workflows.

---

## Step 5 — Repository Layer

Repositories translate business operations into persistence operations.

Responsibilities include:

- INSERT
- UPDATE
- DELETE
- SELECT

Repositories know nothing about:

- FastAPI
- AI
- Prompts
- Business workflows

---

## Step 6 — Response Construction

Business objects are converted into API response schemas.

The API returns serialized data to the client.

The response layer should never expose internal implementation details.

---

# 9. Data Flow

The following diagram illustrates the current end-to-end generation process.

```

```text
Client

↓

POST /generation

↓

Generation Route

↓

Generation Workflow

↓

ScriptService

↓

Gemini

↓

Structured Script

↓

ProjectService

↓

Database

↓

ImageService

↓

Pollinations / Gemini

↓

Generated Images

↓

Image Repository

↓

Database

↓

ProjectGenerationResponse

↓

Client
```

---

## Data Ownership

Each layer owns specific data.

API

Owns:

- Request schemas
- Response schemas

Workflow

Owns:

- Execution order

Services

Owns:

- Business rules

Repositories

Owns:

- Persistence

Providers

Owns:

- External communication

Database

Owns:

- Stored entities

This ownership model minimizes accidental coupling.

---

# 10. Component Responsibilities

The application is composed of independent components.

Each component has one clearly defined responsibility.

---

## API

Responsibilities

- Receive requests
- Validate input
- Return responses

Must never:

- Query the database
- Call providers directly
- Implement business rules

---

## Dependencies

Responsibilities

- Construct objects
- Wire dependencies
- Centralize configuration

Must never:

- Execute business logic

---

## Workflows

Responsibilities

- Coordinate services
- Define execution order

Must never:

- Contain persistence logic
- Build prompts
- Call SQLAlchemy directly

---

## Services

Responsibilities

- Implement business rules
- Validate operations
- Coordinate repositories when needed

Must never:

- Handle HTTP
- Parse requests
- Return FastAPI responses

---

## Repositories

Responsibilities

- Persist entities
- Retrieve entities

Must never:

- Generate AI content
- Build prompts
- Execute workflows

---

## Providers

Responsibilities

- Communicate with external AI APIs

Must never:

- Import FastAPI
- Access SQLAlchemy
- Read application configuration directly
- Know anything about projects or repositories

---

# 11. Project Structure

The backend follows a feature-oriented layered structure.

```

```text
app/

├── api/
│   HTTP interface
│
├── core/
│   Configuration
│   Logging
│   Exceptions
│
├── middleware/
│   HTTP middleware
│
├── dependencies/
│   Dependency Injection
│
├── workflows/
│   Business orchestration
│
├── services/
│   Business logic
│
├── repositories/
│   Database access
│
├── providers/
│   External AI providers
│
├── prompts/
│   Prompt builders
│
├── schemas/
│   API contracts
│
├── db/
│   Models
│   Session
│
└── main.py
```

---

## Folder Responsibilities

### api/

Application entry point.

Contains routes only.

---

### dependencies/

Creates application objects.

Acts as the composition root of the backend.

---

### workflows/

Coordinates multiple services.

Represents complete business use cases.

---

### services/

Contains all business logic.

Every service represents one business capability.

---

### repositories/

Owns persistence.

Implements database operations only.

---

### providers/

Owns external integrations.

Every provider implements one external capability.

---

### prompts/

Contains prompt construction logic.

Prompt engineering remains isolated from business logic.

---

### schemas/

Defines API contracts.

Schemas are independent from SQLAlchemy models.

---

### db/

Contains persistence models and database configuration.

This layer represents storage, not business behavior.
---

# 12. Architectural Decision Records (ADR)

This section documents the major architectural decisions made throughout the project.

Recording these decisions helps future contributors understand *why* the architecture evolved in a particular direction.

---

## ADR-001

### Decision

Separate Text Providers from Image Providers.

### Status

Accepted

### Reason

Different AI vendors specialize in different capabilities.

Text generation and image generation evolve independently and should not be coupled behind a single implementation.

### Consequences

Benefits:

- Independent provider replacement
- Easier testing
- Better scalability
- Clearer abstractions

---

## ADR-002

### Decision

Introduce the Repository Layer.

### Status

Accepted

### Reason

Database operations should remain isolated from business logic.

Repositories provide a stable persistence abstraction regardless of database implementation.

### Consequences

Benefits:

- Cleaner services
- Easier testing
- Database independence
- Improved maintainability

---

## ADR-003

### Decision

Introduce the Workflow Layer.

### Status

Accepted

### Reason

Business processes often require multiple services.

Workflows coordinate services while keeping business rules inside their respective services.

### Consequences

Benefits:

- Clear orchestration
- Reusable services
- Reduced service coupling

---

## ADR-004

### Decision

Centralize Dependency Injection.

### Status

Accepted

### Reason

Object creation should occur in one location.

Services should receive collaborators through constructor injection.

### Consequences

Benefits

- Testability
- Replaceability
- Cleaner architecture

---

## ADR-005

### Decision

Separate Business Logic from Framework Logic.

### Status

Accepted

### Reason

Business rules should not depend on FastAPI or infrastructure details.

Frameworks may change.

Business rules should not.

---

# 13. Current Implementation Status

## Completed

### Core

- FastAPI application
- Configuration management
- Logging
- Exception handling
- Middleware

---

### Persistence

- SQLAlchemy models
- Async sessions
- Alembic migrations
- Repository layer

---

### Business Layer

- ProjectService
- ScriptService
- ImageService
- GeneratedImageService
- AIService

---

### AI

- Structured text generation
- Prompt builders
- Image generation
- Provider abstraction

---

### Storage

- Local image persistence
- Static file serving

---

### Workflows

- End-to-end generation workflow

Current execution pipeline:

Generate Script

↓

Persist Project

↓

Generate Images

↓

Persist Images

↓

Return Complete Project

---

# 14. Planned Evolution

The architecture intentionally anticipates future capabilities.

Planned additions include:

- Voice generation
- Subtitle generation
- Thumbnail generation
- Video timeline creation
- Video rendering
- FFmpeg integration
- Background jobs
- Queue processing
- Cloud storage
- Authentication
- Team workspaces
- Usage tracking
- Billing
- Publishing integrations

These features should integrate into existing architectural boundaries instead of introducing parallel structures.

---

# 15. Development Rules

Every contribution to the project must respect the following rules.

---

## API Rules

Routes should:

- Validate requests
- Resolve dependencies
- Delegate execution
- Return responses

Routes must never:

- Execute SQL
- Build prompts
- Implement business logic

---

## Workflow Rules

Workflows should:

- Coordinate services
- Define execution order

Workflows must never:

- Persist entities directly
- Access repositories directly
- Communicate with AI providers directly

---

## Service Rules

Services should:

- Own business rules
- Validate business operations
- Coordinate repositories when necessary

Services must never:

- Return HTTP responses
- Import FastAPI routing components
- Contain presentation logic

---

## Repository Rules

Repositories should:

- Persist entities
- Query entities
- Update entities
- Delete entities

Repositories must never:

- Generate AI content
- Validate business rules
- Coordinate workflows

---

## Provider Rules

Providers should:

- Communicate with external services
- Translate provider responses

Providers must never:

- Import SQLAlchemy
- Import FastAPI
- Know application business models

---

## Schema Rules

Schemas represent contracts between the API and its consumers.

Schemas are not database models.

Schemas should remain framework-independent whenever possible.

---

# 16. Coding Principles

The project follows the following engineering principles.

- Single Responsibility Principle
- Separation of Concerns
- Dependency Injection
- Composition over Inheritance
- Explicit Dependencies
- Small Focused Services
- Provider Isolation
- Repository Pattern
- Incremental Evolution
- Readability over Cleverness

Whenever architectural decisions conflict with convenience, architecture takes precedence.

---

# 17. Milestones

## Milestone 1

Completed

- Project foundation
- Database
- Repository layer
- AI abstraction

---

## Milestone 2

Completed

- Script generation
- Image generation
- Image persistence
- End-to-end generation workflow
- Dependency Injection architecture
- Workflow architecture

---

## Milestone 3

Planned

- Voice generation
- Audio provider abstraction
- Voice workflow integration

---

## Milestone 4

Planned

- Subtitle generation
- Timeline synchronization

---

## Milestone 5

Planned

- Video rendering
- FFmpeg integration
- Export pipeline

---

# 18. Long-Term Architecture Vision

The long-term objective of ShortForge is to transform a single user request into a complete, production-ready short-form video.

The final execution pipeline is expected to become:

```

```text
Idea

↓

Generate Script

↓

Persist Project

↓

Generate Images

↓

Generate Thumbnail

↓

Generate Voice

↓

Generate Subtitles

↓

Build Timeline

↓

Render Video

↓

Export Assets

↓

Publish
```

The architecture should evolve through extension rather than redesign.

Each new capability should integrate into existing architectural boundaries while preserving the principles defined in this document.

---

# 19. Conclusion

This document defines the architectural foundation of ShortForge.

It serves as the reference for all future backend development.

Every architectural change should preserve the following goals:

- Maintain clear boundaries.
- Keep business logic independent.
- Prefer explicit dependencies.
- Design for extension instead of modification.
- Keep the architecture understandable as the system grows.

When implementation and architecture diverge, the discrepancy should be resolved immediately by updating either the code or this document.

---

**End of Document**