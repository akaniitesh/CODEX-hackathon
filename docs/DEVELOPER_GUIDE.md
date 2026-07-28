# Autonomous Software Engineering Platform: Developer Guide

> **Target Audience**: This guide is written for software engineers joining the project. It provides an exhaustive, end-to-end technical walkthrough of the codebase architecture, request lifecycles, data flows, extension patterns, and step-by-step developer workflows.

---

## Table of Contents
1. [Architecture & Request Lifecycle](#1-architecture--request-lifecycle)
2. [Backend Architecture](#2-backend-architecture)
3. [Frontend Architecture](#3-frontend-architecture)
4. [AI Provider & Orchestration Architecture](#4-ai-provider--orchestration-architecture)
5. [Repository Analysis Engine](#5-repository-analysis-engine)
6. [Security & Hardening Architecture](#6-security--hardening-architecture)
7. [Celery Workers & Realtime WebSockets](#7-celery-workers--realtime-websockets)
8. [Directory Structure Deep Dive](#8-directory-structure-deep-dive)
9. [API Endpoints Reference](#9-api-endpoints-reference)
10. [Configuration & Environment Reference](#10-configuration--environment-reference)
11. [Debugging & Developer Workflows](#11-debugging--developer-workflows)
12. [How to Extend the Platform](#12-how-to-extend-the-platform)
13. [Tutorial: Contributing Your First Feature](#13-tutorial-contributing-your-first-feature)

---

# 1. Architecture & Request Lifecycle

The platform couples a **FastAPI async backend** with a **Next.js 16 App Router frontend**, **Celery background workers**, a **LangGraph state engine**, and a multi-provider **AI Abstraction Layer**.

### End-to-End Request Lifecycle
```mermaid
sequenceDiagram
    autonumber
    actor User as Developer / Browser
    participant FE as Next.js 16 Frontend
    participant Nginx as Nginx Proxy (:80)
    participant FastAPI as FastAPI Router (:8000)
    participant Auth as Security / JWT Layer
    participant Service as Business Service Layer
    participant DB as PostgreSQL Database
    participant Celery as Celery Worker
    participant Graph as LangGraph State Engine
    participant AI as AI Provider Abstraction

    User->>FE: Click "Launch Run" / Interactive Action
    FE->>Nginx: POST /api/v1/runs
    Nginx->>FastAPI: Forward Request
    FastAPI->>Auth: decode_access_token() & require_role()
    Auth-->>FastAPI: User Principal Validated
    FastAPI->>Service: RunService.create_run()
    Service->>DB: INSERT Into runs Table (Async SQLAlchemy)
    DB-->>Service: Run Record Created (ID: run-123)
    Service->>Celery: enqueue_run.delay("run-123")
    Service-->>FE: HTTP 202 Accepted {"run_id": "run-123", "status": "queued"}
    Celery->>Graph: Execute StateGraph(AutonomousAgentState)
    Graph->>AI: FallbackAIProvider.generate(request)
    AI-->>Graph: AIResponse (Gemini / OpenAI / Groq / Ollama)
    Graph->>Service: Update Run Execution State
    Service->>FE: WebSocket Push Event ("status_changed")
```

---

# 2. Backend Architecture

The backend ([backend/app](file:///d:/Codex%20Hackathon/backend/app)) is built on FastAPI using a clean **Layered Architecture**:

```
FastAPI Routers (HTTP / WebSockets)
       │
       ▼
Dependencies & Auth Layer (JWT / RBAC / RateLimiter)
       │
       ▼
Service Layer (Business Rules & Orchestration)
       │
       ▼
Repository Data Access Layer (BaseRepository / SQLAlchemy)
       │
       ▼
Database Engine (AsyncPG + PostgreSQL 16)
```

### FastAPI Routing & Dependency Injection
- **Versioned Routers**: All REST endpoints are declared in `app/api/v1/routers/` and registered into `api_router` ([router.py](file:///d:/Codex%20Hackathon/backend/app/api/v1/router.py)).
- **Dependency Injection**: Database sessions (`get_db_session`), current user authorization (`get_current_user`), and settings (`get_settings`) are injected dynamically via FastAPI `Depends()`.

```python
# Example: FastAPI Dependency Injection Route Pattern
@router.get("/repositories", response_model=Page[RepositoryRead])
async def list_repositories(
    limit: int = 50,
    offset: int = 0,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> Page[RepositoryRead]:
    repo_service = RepositoryService(db)
    return await repo_service.list_repositories(limit=limit, offset=offset)
```

### Repository & Service Layer
- **Repository Pattern**: Extends `BaseRepository[T]` ([base_repository.py](file:///d:/Codex%20Hackathon/backend/app/repositories/base_repository.py)) providing generic async CRUD operations (`get_by_id`, `list_all`, `create`, `update`, `delete`).
- **Service Layer**: Business services ([app/services](file:///d:/Codex%20Hackathon/backend/app/services)) encapsulate multi-repository operations, external integrations, and task scheduling.

### Database Models (SQLAlchemy ORM)
All models inherit from `Base` ([base.py](file:///d:/Codex%20Hackathon/backend/app/db/base.py)) and include timestamp mixins:
- `User`: Application users, role designations (`OWNER`, `ADMIN`, `MEMBER`, `VIEWER`), and GitHub user IDs.
- `Organization`: Organization tenants.
- `Membership`: User-to-Organization membership joins.
- `Repository`: Connected GitHub repositories, clone URLs, default branches, and active status flags.
- `Run`: Execution runs, commit SHAs, webhook delivery IDs, and execution statuses (`queued`, `running`, `completed`, `failed`).
- `Execution`: Individual agent execution step snapshots.
- `TimelineEvent`: Granular step timeline events for real-time streaming.
- `Artifact`: Generated documentation and code diff proposals.

---

# 3. Frontend Architecture

The frontend ([frontend/](file:///d:/Codex%20Hackathon/frontend)) is built with **Next.js 16 App Router**, **TypeScript**, **Tailwind CSS**, **Zustand**, and **React Query**:

```
Next.js App Router (app/layout.tsx, app/page.tsx)
       │
       ▼
Global App Shell (AppShell.tsx & Navbar.tsx)
       │
       ├──► Repository List Panel (RepositoryList.tsx)
       └──► Cost & Telemetry Analytics Panel (AnalyticsPanel.tsx)
       │
       ▼
Zustand State Stores (useAuthStore, useRepoStore)
       │
       ▼
API Client Layer (src/lib/api.ts -> REST & WebSockets)
```

### Frontend State Management & API Integration
- **Zustand Auth Store** ([useAuthStore.ts](file:///d:/Codex%20Hackathon/frontend/src/store/useAuthStore.ts)): Stores JWT tokens in `localStorage`, tracks user profile metadata, and toggles login modals.
- **Zustand Repo Store** ([useRepoStore.ts](file:///d:/Codex%20Hackathon/frontend/src/store/useRepoStore.ts)): Manages the currently selected repository, active panel tab (`repositories`, `timeline`, `graph`, `reviews`, `architecture`, `analytics`), and connect modal toggles.
- **React Query** ([QueryProvider.tsx](file:///d:/Codex%20Hackathon/frontend/src/providers/QueryProvider.tsx)): Manages asynchronous data fetching, automatic background refetching (5s interval on telemetry), and stale-time caching.
- **API Client** ([api.ts](file:///d:/Codex%20Hackathon/frontend/src/lib/api.ts)): Wraps native `fetch` requests with automatic `Authorization: Bearer <token>` injection and JSON error parsing.

---

# 4. AI Provider & Orchestration Architecture

### AI Provider Abstraction
The AI abstraction layer ([app/ai](file:///d:/Codex%20Hackathon/backend/app/ai)) decouples vendor SDKs from application business logic:

```mermaid
flowchart TD
    Agent[LangGraph Agent Node] --> Request[AIRequest]
    Request --> Factory{AIProviderFactory}
    Factory -->|Select AI_PROVIDER| Fallback[FallbackAIProvider]
    
    subgraph Circuit Breakers & Key Rotation
        Fallback --> Breaker1{Gemini Breaker}
        Breaker1 -->|Closed| Gemini[GeminiProvider]
        Breaker1 -->|Open / Tripped| Breaker2{OpenAI Breaker}
        Breaker2 -->|Closed| OpenAI[OpenAIProvider]
        Breaker2 -->|Open / Tripped| Breaker3{Groq Breaker}
        Breaker3 -->|Closed| Groq[GroqProvider]
        Breaker3 -->|Open / Tripped| Breaker4{Ollama Breaker}
        Breaker4 -->|Closed| Ollama[OllamaProvider]
    end
    
    Gemini --> Response[AIResponse / StreamChunk]
    OpenAI --> Response
    Groq --> Response
    Ollama --> Response
```

- **Base Interface** (`BaseAIProvider`): Defines `generate()`, `stream()`, and `structured_output()` methods.
- **HttpChatProvider**: Base class for OpenAI-compatible REST API providers.
- **Concrete Providers**: `GeminiProvider`, `OpenAIProvider`, `GroqProvider`, `OllamaProvider`.
- **ApiKeyRing**: Round-robin API key rotation manager.
- **TokenBudgetManager**: Enforces token limit and USD cost ceilings per run and user.
- **CircuitBreaker**: 3-state breaker (`CLOSED`, `OPEN`, `HALF_OPEN`) tracking failure thresholds and cooldown windows.

### LangGraph Agent Engine & Foundation
- **State Schema** (`AutonomousAgentState` in [schemas.py](file:///d:/Codex%20Hackathon/backend/app/agents/schemas.py)): TypedDict tracking `run_id`, `repository_id`, `current_step`, `step_count`, `repo_summary`, `execution_plan`, `errors`, and `messages`. Uses `add_messages` and `add_errors` reducers.
- **Prompt Registry** (`PromptRegistry` in [registry.py](file:///d:/Codex%20Hackathon/backend/app/agents/prompts/registry.py)): Loads versioned text templates from `templates/` (`planner_v1.txt`, `repo_analyzer_v1.txt`, etc.) and validates template formatting placeholders.
- **Tool Permission System** (`ToolPermissionManager` in [permissions.py](file:///d:/Codex%20Hackathon/backend/app/agents/permissions.py)): Enforces declarative agent-to-tool allowlists (`AGENT_TOOL_ALLOWLIST`). Disallowed tool calls raise HTTP 403 `ToolPermissionDeniedError`.
- **StateGraph Skeleton** (`build_graph_skeleton()` in [graph.py](file:///d:/Codex%20Hackathon/backend/app/agents/graph.py)): Links agent node placeholders from `START` to `END`.

---

# 5. Repository Analysis Engine

The repository analysis engine ([app/analysis](file:///d:/Codex%20Hackathon/backend/app/analysis)) performs deterministic, non-evaluative code analysis:

1. **Directory Tree Service** (`DirectoryTreeService`): Generates bounded directory inventories while filtering out sensitive files (`.env`, `.pem`, `id_rsa`).
2. **README Service** (`ReadmeService`): Locates and extracts project README overview text.
3. **Tree-Sitter Discovery** (`TreeSitterAstService`): Identifies language targets across files.
4. **Python Import Graph** (`ImportGraphService`): Parses Python AST to extract top-level import dependencies, class definitions, and function signatures.
5. **Git History Service** (`GitHistoryService`): Uses GitPython to safely extract recent commit metadata.
6. **Static Analysis Service** (`StaticAnalysisService`): Wraps Ruff, Bandit, Semgrep, and Radon via `asyncio.create_subprocess_exec` with `shell=False` and strict timeouts.
7. **Repository Summarizer** (`RepositorySummarizer`): Synthesizes analytical summaries into a JSON payload and caches results in Redis keyed by commit SHA.

---

# 6. Security & Hardening Architecture

- **JWT Authentication** ([security.py](file:///d:/Codex%20Hackathon/backend/app/core/security.py)): Generates and decodes JWT tokens signed with a 32-byte secret key using `HS256`.
- **GitHub Webhook Verification** (`verify_github_signature`): Verifies HMAC SHA256 signatures (`X-Hub-Signature-256`) against raw request bodies before JSON parsing.
- **Secret Sanitizer** (`SecretSanitizer` in [sanitizer.py](file:///d:/Codex%20Hackathon/backend/app/core/sanitizer.py)): Applies regex filters masking API keys (`sk-...`, `gsk_...`), GitHub tokens (`ghp_...`), Bearer tokens, passwords, and `.env` credentials in all log outputs and AI payloads.
- **Rate Limiting** (`RateLimiter` in [security_hardening.py](file:///d:/Codex%20Hackathon/backend/app/core/security_hardening.py)): Sliding window token bucket middleware enforcing a default limit of 120 requests/min per IP.
- **Security Headers** (`SecurityHeadersMiddleware`): Sets Helmet-equivalent response headers (`nosniff`, `DENY`, `1; mode=block`, `HSTS`).
- **Audit Logger** (`AuditLogger` in [audit.py](file:///d:/Codex%20Hackathon/backend/app/core/audit.py)): Append-only logger recording structured audit events for governance.

---

# 7. Celery Workers & Realtime WebSockets

- **Celery Configuration** ([celery_app.py](file:///d:/Codex%20Hackathon/backend/app/workers/celery_app.py)): Configures Redis as the message broker (`redis://localhost:6379/0`) and result backend with `runs` and `dead_letter` queues.
- **Dead-Letter Routing** ([tasks.py](file:///d:/Codex%20Hackathon/backend/app/workers/tasks.py)): Extends `DeadLetterTask` on-failure handlers to route exhausted task failures to the `dead_letter` queue without exposing sensitive payloads.
- **WebSocket Push Manager** (`WebSocketManager` in [websocket_manager.py](file:///d:/Codex%20Hackathon/backend/app/services/websocket_manager.py)): Manages active channel connections (e.g. `run:run-123`) and broadcasts JSON events (`status_changed`, `step_completed`).

---

# 8. Directory Structure Deep Dive

```
backend/app/
├── agents/             # LangGraph state schema, prompt registry, tool allowlists, & state graph
│   ├── prompts/        # PromptRegistry and versioned text templates (planner_v1.txt, etc.)
│   ├── graph.py        # LangGraph StateGraph skeleton construction
│   ├── permissions.py  # ToolPermissionManager and agent allowlists
│   └── schemas.py      # AutonomousAgentState and prompt/permission Pydantic models
├── ai/                 # Multi-provider LLM abstraction layer
│   ├── base.py         # BaseAIProvider abstract interface
│   ├── budget.py       # TokenBudgetManager token & cost limit tracking
│   ├── circuit_breaker.py # 3-state CircuitBreaker machine
│   ├── factory.py      # AIProviderFactory and fallback provider chain generator
│   ├── fallback.py     # FallbackAIProvider resilient fallback execution
│   ├── http_provider.py# HttpChatProvider base class for OpenAI-compatible REST APIs
│   ├── keyring.py      # ApiKeyRing round-robin API key rotation
│   ├── providers.py    # GeminiProvider, OpenAIProvider, GroqProvider, OllamaProvider
│   └── schemas.py      # AIRequest, AIResponse, StreamChunk, TokenUsage schemas
├── analysis/           # Codebase analysis services
│   ├── git_history.py  # GitPython recent commit summaries
│   ├── import_graph.py # Python AST import & symbol extraction
│   ├── readme_service.py # README text finder & loader
│   ├── safety.py       # Secret file exclusion & path traversal safety filters
│   ├── static_tools.py # Ruff, Bandit, Semgrep, & Radon async subprocess wrappers
│   ├── summarizer.py   # RepositorySummarizer Redis SHA-keyed summarization
│   └── tree_service.py # DirectoryTreeService & TreeSitterAstService target finder
├── api/                # REST & WebSocket interface layer
│   ├── dependencies.py # FastAPI DB session & auth user dependency injection
│   └── v1/
│       ├── endpoints/  # Telemetry & Prometheus metrics router
│       ├── routers/    # Auth, Health, Repositories, Runs, Webhooks, WS routers
│       └── router.py   # Combined versioned API router (/api/v1)
├── core/               # Platform cross-cutting utilities
│   ├── audit.py        # Append-only AuditLogger
│   ├── config.py       # Pydantic BaseSettings environment configuration
│   ├── errors.py       # Standardized ApiError exception hierarchy
│   ├── metrics.py      # Prometheus counters, gauges, & histograms
│   ├── sanitizer.py    # SecretSanitizer credential masking regex filter
│   ├── security.py     # JWT encoding/decoding & GitHub HMAC verification
│   └── security_hardening.py # Security headers middleware & RateLimiter
├── db/                 # Database engine & base models
│   ├── base.py         # Declarative Base metadata
│   └── session.py      # Async SQLAlchemy engine & async_sessionmaker factory
├── models/             # SQLAlchemy ORM database entity models
├── repositories/       # Data Access Object repository classes
├── schemas/            # Pydantic request/response validation schemas
├── services/           # Application business logic services
└── workers/            # Celery application & worker task definitions
```

---

# 9. API Endpoints Reference

### Health & Telemetry
- `GET /api/v1/health`: Checks process health.
- `GET /api/v1/health/db`: Checks PostgreSQL database connection.
- `GET /api/v1/metrics/prometheus`: Exports Prometheus plaintext metrics.
- `GET /api/v1/telemetry/health`: Returns JSON AI provider states, token costs, and audit metrics.

### Authentication & Repositories
- `GET /api/v1/auth/github/start`: Generates GitHub OAuth authorization URL.
- `POST /api/v1/auth/github/callback`: Exchanges OAuth authorization code for JWT token.
- `GET /api/v1/repositories`: Returns paginated list of connected repositories.
- `POST /api/v1/repositories`: Connects a new GitHub repository.

### Execution Runs & Webhooks
- `POST /api/v1/webhooks/github`: Receives HMAC SHA256 verified GitHub webhooks.
- `GET /api/v1/runs/repositories/{id}`: Returns execution runs for a repository.
- `POST /api/v1/runs`: Manually triggers a new autonomous execution run.
- `WS /api/v1/ws/connect`: Authenticated WebSocket endpoint for real-time event streaming.

---

# 10. Configuration & Environment Reference

### Key Environment Variables (`backend/.env`)

```ini
ENV=development
DATABASE_URL=postgresql+asyncpg://autose_user:autose_password@localhost:5432/autose_platform
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=change-this-to-a-secure-32-character-random-key
WEBHOOK_SECRET=change-this-to-a-secure-webhook-secret
AI_PROVIDER=gemini
GOOGLE_API_KEY=AIzaSy...
MODEL_NAME=gemini-1.5-flash
OPENAI_API_KEYS=sk-proj-123,sk-proj-456
GROQ_API_KEYS=gsk_123,gsk_456
```

---

# 11. Debugging & Developer Workflows

### Running Backend Unit & Integration Tests
```bash
cd backend
pytest -v
```

### Running Golden Regression Tests
```bash
cd backend
pytest tests/test_golden_regression.py -v
```

### Running Static Linters & Type Checking
```bash
cd backend
ruff check app tests
mypy app tests
```

---

# 12. How to Extend the Platform

### A. How to Add a New AI Provider
1. Add new provider enum value in `app/ai/schemas.py`:
   ```python
   class ProviderName(StrEnum):
       MISTRAL = "mistral"
   ```
2. Create provider class in `app/ai/providers.py`:
   ```python
   class MistralProvider(HttpChatProvider):
       def __init__(self, api_keys: list[str], model: str) -> None:
           super().__init__(
               name=ProviderName.MISTRAL,
               base_url="https://api.mistral.ai/v1",
               default_model=model,
               keyring=ApiKeyRing(api_keys),
           )
   ```
3. Register provider in `_provider_map()` inside `app/ai/factory.py`.

### B. How to Add a New API Endpoint
1. Declare request/response schemas in `app/schemas/`.
2. Implement router logic in `app/api/v1/routers/`.
3. Register the router in `app/api/v1/router.py`.

### C. How to Add a New Frontend Page / Tab
1. Add tab ID to `RepoState['activeTab']` in `frontend/src/store/useRepoStore.ts`.
2. Add navigation item in `frontend/src/components/layout/Navbar.tsx`.
3. Create panel component in `frontend/src/components/` and render it inside `AppShell.tsx`.

---

# 13. Tutorial: Contributing Your First Feature

In this step-by-step tutorial, you will add a new **"Repository Stats Aggregator"** feature that exposes repository line count metrics via a new backend REST endpoint and displays them on the frontend.

### Step 1: Branch Creation
```bash
git checkout -b feature/repo-stats-aggregator
```

### Step 2: Create Pydantic Schema
In `backend/app/schemas/repository.py`, add:
```python
class RepositoryStatsResponse(BaseModel):
    repository_id: str
    total_files: int
    total_symbols: int
```

### Step 3: Implement Service Function
In `backend/app/services/repository_service.py`, add:
```python
async def get_repository_stats(self, repository_id: str) -> RepositoryStatsResponse:
    # Business logic calculating repository statistics
    return RepositoryStatsResponse(
        repository_id=repository_id,
        total_files=42,
        total_symbols=156,
    )
```

### Step 4: Expose FastAPI Route
In `backend/app/api/v1/routers/repositories.py`, add:
```python
@router.get("/{id}/stats", response_model=RepositoryStatsResponse)
async def get_repository_stats(
    id: str,
    db: AsyncSession = Depends(get_db_session),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> RepositoryStatsResponse:
    service = RepositoryService(db)
    return await service.get_repository_stats(id)
```

### Step 5: Write Pytest Unit Test
In `backend/tests/test_api_routes.py`, add:
```python
@pytest.mark.asyncio
async def test_get_repository_stats_endpoint(async_client: AsyncClient) -> None:
    res = await async_client.get("/api/v1/repositories/repo-123/stats")
    assert res.status_code == 200
    assert res.json()["total_files"] == 42
```

### Step 6: Verify Tests, Linter, and Type Checker
```bash
cd backend
pytest -v
ruff check app tests
mypy app tests
```

### Step 7: Update Frontend API Client
In `frontend/src/lib/api.ts`, add:
```typescript
getRepoStats: (repositoryId: string) =>
  request<{ repository_id: string; total_files: number; total_symbols: number }>(
    `/repositories/${repositoryId}/stats`
  ),
```

### Step 8: Commit and Push
```bash
git add .
git commit -m "feat(repo): add repository stats aggregator endpoint and frontend API client"
git push origin feature/repo-stats-aggregator
```
