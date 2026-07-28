# Feature Matrix

This document compares the project vision evidenced inside this repository with the actual implementation present in code today.

Source note: no standalone original specification or requirements document exists in the repository. This matrix therefore uses only repository evidence: `DEPLOYMENT_RUNBOOK.md`, `backend/README.md`, prompt templates, UI labels, API helpers, tests, and implementation files. Generated dependency/build/cache folders such as `frontend/node_modules`, `frontend/.next`, Python caches, and `.git` metadata are excluded from feature status decisions.

## Legend

✅ Implemented

🟡 Partial

⚪ Deferred

❌ Missing

---

## Core Platform

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Repository connection | 🟡 Partial | `backend/app/models/repository.py`, `backend/app/api/v1/routers/repositories.py`, `frontend/src/components/auth/ConnectRepoModal.tsx` | Repository model and list endpoint exist. The frontend connect modal only creates local state. No backend create/connect endpoint exists. |
| GitHub OAuth | 🟡 Partial | `backend/app/api/v1/routers/auth.py`, `backend/app/services/auth_service.py`, `frontend/src/components/auth/LoginModal.tsx` | Backend can build a GitHub authorization URL and exchange a code. User persistence and OAuth state validation are not implemented. Frontend login remains demo/local. |
| JWT Authentication | ✅ Implemented | `backend/app/core/security.py`, `backend/app/api/v1/routers/*.py`, `backend/tests/test_api_auth.py` | JWT creation, decoding, role dependency, REST route protection, telemetry protection, and WebSocket token validation exist. |
| RBAC | 🟡 Partial | `backend/app/core/security.py`, `backend/app/models/membership.py` | Role hierarchy and route guards exist. Repository and organization membership scoping is not enforced. |
| Repository Analysis | 🟡 Partial | `backend/app/analysis/*`, `backend/tests/test_analysis_tools.py` | Deterministic tree, README, Python import/symbol, Git history, and static tool wrappers exist. The pipeline is not wired into worker or agent execution. |
| Execution Planning | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/planner_v1.txt` | Planner prompt and placeholder graph node exist. No real planning call or structured plan persistence is implemented. |
| Pull Request Generation | 🟡 Partial | `backend/app/models/pull_request.py`, `backend/app/agents/prompts/templates/pr_generator_v1.txt`, `backend/app/agents/graph.py` | Model, prompt, and placeholder node exist. No PR generation or GitHub PR creation flow exists. |
| Documentation Generation | 🟡 Partial | `backend/app/models/artifact.py`, `backend/app/agents/prompts/templates/documentation_v1.txt`, `backend/app/agents/graph.py` | Artifact model, prompt, and placeholder node exist. No generator execution exists. |
| Architecture Analysis | 🟡 Partial | `backend/app/agents/prompts/templates/architecture_v1.txt`, `backend/app/agents/graph.py` | Prompt and placeholder node exist. No actual architecture analysis is run. |
| Code Review | 🟡 Partial | `backend/app/agents/prompts/templates/code_reviewer_v1.txt`, `backend/app/agents/graph.py`, `backend/app/analysis/static_tools.py` | Prompt, placeholder node, and static tool wrappers exist. No integrated review result is generated. |
| Test Generation | 🟡 Partial | `backend/app/agents/prompts/templates/test_generator_v1.txt`, `backend/app/agents/graph.py` | Prompt and placeholder node exist. No runnable generated tests are produced. |
| Security Analysis | 🟡 Partial | `backend/app/agents/prompts/templates/security_auditor_v1.txt`, `backend/app/analysis/static_tools.py`, `backend/app/agents/graph.py` | Prompt, placeholder node, and Bandit/Semgrep wrappers exist. No integrated security audit workflow exists. |
| Deployment Validation | ❌ Missing | `backend/app/agents/permissions.py` | Only a tool allowlist entry exists. No graph node, service, prompt, or API exists. |
| Agent Timeline | 🟡 Partial | `backend/app/models/timeline_event.py`, `backend/app/models/execution.py` | Timeline and execution models exist. No worker/agent writes timeline events. |
| WebSocket Updates | 🟡 Partial | `backend/app/api/v1/routers/ws.py`, `backend/app/services/websocket_manager.py` | Authenticated WebSocket endpoint and in-process manager exist. No worker or agent broadcasts run events. |
| Dashboard | 🟡 Partial | `frontend/src/components/layout/AppShell.tsx`, `frontend/src/components/repositories/RepositoryList.tsx`, `frontend/src/components/analytics/AnalyticsPanel.tsx` | Dashboard shell exists, but most data is mock/local and several tabs render no view. |

---

## AI Providers

| Provider | Chat | Streaming | Structured Output | Provider Factory | Circuit Breaker | Retry | API Key Rotation | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| OpenAI | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 | ✅ | Uses `OpenAIProvider` over `HttpChatProvider`; breaker/retry apply through `FallbackAIProvider` and are in-memory. |
| Gemini | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 | ✅ | Uses Gemini OpenAI-compatible endpoint; Google key fallback is supported. |
| Groq | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 | ✅ | Uses Groq OpenAI-compatible endpoint; fallback chain includes it. |
| Ollama | ✅ | ✅ | ✅ | ✅ | 🟡 | 🟡 | ✅ | Uses local OpenAI-compatible endpoint. API key rotation is effectively not needed because `ApiKeyRing([])` omits authorization headers. |

Locations: `backend/app/ai/base.py`, `backend/app/ai/providers.py`, `backend/app/ai/http_provider.py`, `backend/app/ai/factory.py`, `backend/app/ai/fallback.py`, `backend/app/ai/circuit_breaker.py`, `backend/app/ai/retry.py`, `backend/app/ai/keyring.py`.

---

## Embedding Providers

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Gemini Embeddings | ❌ Missing | N/A | No embedding provider abstraction or Gemini embedding implementation exists. |
| OpenAI Embeddings | ❌ Missing | N/A | No OpenAI embedding implementation exists. |
| FastEmbed | ❌ Missing | N/A | No FastEmbed dependency or implementation exists. |
| Sentence Transformers | ❌ Missing | N/A | No sentence-transformers dependency or implementation exists. |
| Batch Embeddings | ❌ Missing | N/A | No batch embedding API exists. |
| Query Embeddings | ❌ Missing | N/A | No query embedding API exists. |
| Document Embeddings | ❌ Missing | N/A | No document embedding pipeline exists. |
| Embedding Cache | ❌ Missing | N/A | Redis caches repository summaries only, not embeddings. |
| Dimension Validation | ❌ Missing | N/A | No vector dimension validation exists. |

---

## LangGraph

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Planner | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/planner_v1.txt` | Placeholder node sets `current_step`; prompt exists. |
| Repository Analyzer | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/repo_analyzer_v1.txt` | Placeholder node exists; repository analysis services are separate and not called by the node. |
| Architecture Agent | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/architecture_v1.txt` | Placeholder node and prompt exist. |
| Code Reviewer | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/code_reviewer_v1.txt` | Placeholder node and prompt exist. |
| Test Generator | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/test_generator_v1.txt` | Placeholder node and prompt exist. |
| Security Auditor | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/security_auditor_v1.txt` | Placeholder node and prompt exist. |
| Documentation Agent | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/documentation_v1.txt` | Placeholder node and prompt exist. |
| PR Generator | 🟡 Partial | `backend/app/agents/graph.py`, `backend/app/agents/prompts/templates/pr_generator_v1.txt` | Placeholder node and prompt exist. |
| Deployment Validator | ❌ Missing | `backend/app/agents/permissions.py` | Only an allowlist entry exists. |
| Memory Manager | ❌ Missing | `backend/app/agents/permissions.py` | Only an allowlist entry exists. |
| Guardrails | 🟡 Partial | `backend/app/core/sanitizer.py`, `backend/app/core/metrics.py`, `backend/app/agents/permissions.py` | Secret sanitizer, guardrail metric counter, and permission checks exist, but no LangGraph guardrail node or model I/O enforcement exists. |
| Prompt Registry | ✅ Implemented | `backend/app/agents/prompts/registry.py`, `backend/app/agents/prompts/templates/*.txt` | Versioned prompt lookup and variable validation exist. |
| Tool Permission System | 🟡 Partial | `backend/app/agents/permissions.py`, `backend/tests/test_agent_foundation.py` | Permission manager exists and is tested, but no real tool executor uses it. |
| Human Approval | 🟡 Partial | `backend/app/agents/graph.py` | Placeholder node exists. No interrupt, UI approval, or persistence exists. |
| Checkpointing | ❌ Missing | N/A | No LangGraph checkpointer or persisted checkpoint store exists. |
| Execution Replay | ❌ Missing | N/A | No replay API, persisted state snapshots, or replay UI exists. |

---

## Repository Analysis

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Tree-sitter | 🟡 Partial | `backend/app/analysis/tree_service.py` | Service identifies parse targets. It does not load grammars or parse ASTs. Code comments defer installed grammars to future agent tools. |
| GitPython | ✅ Implemented | `backend/app/analysis/git_history.py`, `backend/pyproject.toml` | Recent commit metadata is collected with GitPython. |
| Ruff | 🟡 Partial | `backend/app/analysis/static_tools.py`, `backend/pyproject.toml` | Static wrapper exists. Not wired into agent execution. |
| Pyright | 🟡 Partial | `backend/app/analysis/static_tools.py` | Static wrapper exists, but dependency is not declared in backend Python package. |
| Bandit | 🟡 Partial | `backend/app/analysis/static_tools.py`, `backend/pyproject.toml` | Static wrapper and dependency exist. Not wired into agent execution. |
| Semgrep | 🟡 Partial | `backend/app/analysis/static_tools.py`, `backend/pyproject.toml` | Static wrapper and dependency exist. Not wired into agent execution. |
| Radon | 🟡 Partial | `backend/app/analysis/static_tools.py`, `backend/pyproject.toml` | Static wrapper and dependency exist. Not wired into agent execution. |
| Chunking | ❌ Missing | N/A | No chunking service or token-aware file chunker exists. |
| Summarization | ✅ Implemented | `backend/app/analysis/summarizer.py` | Deterministic repository summary composition and Redis caching exist. |
| Dependency Graph | 🟡 Partial | `backend/app/analysis/import_graph.py` | Python top-level import graph exists. No full dependency graph across package managers/languages exists. |
| AST Parsing | 🟡 Partial | `backend/app/analysis/import_graph.py`, `backend/app/analysis/tree_service.py` | Python AST is parsed for imports/symbols; Tree-sitter parsing is target discovery only. |
| README Analysis | ✅ Implemented | `backend/app/analysis/readme_service.py` | Bounded README collection exists. |
| Git History | ✅ Implemented | `backend/app/analysis/git_history.py` | Latest commit summaries are collected. |

---

## Security

| Feature | Status | Location | Notes |
|---|---:|---|---|
| JWT | ✅ Implemented | `backend/app/core/security.py`, `backend/tests/test_api_auth.py` | Token creation, decode, expiry, and bearer dependency exist. |
| OAuth | 🟡 Partial | `backend/app/services/auth_service.py`, `backend/app/api/v1/routers/auth.py` | GitHub OAuth start/callback exists. State validation and persisted identity are missing. |
| RBAC | 🟡 Partial | `backend/app/core/security.py`, `backend/app/models/membership.py` | Role checks exist. Tenant/repository authorization is missing. |
| Rate Limiting | ✅ Implemented | `backend/app/core/security_hardening.py`, `backend/app/main.py` | In-memory per-IP limiter is wired as middleware. |
| Webhook Verification | ✅ Implemented | `backend/app/core/security.py`, `backend/app/api/v1/routers/webhooks.py` | GitHub HMAC SHA-256 verification happens before JSON parsing. |
| Prompt Injection Protection | 🟡 Partial | `backend/app/core/sanitizer.py`, `backend/app/ai/structured.py` | Secret redaction and strict JSON retry exist. No comprehensive prompt-injection policy or repository-content isolation exists. |
| Indirect Prompt Injection | ❌ Missing | N/A | No explicit indirect prompt-injection detection or quarantine exists. |
| Secrets Management | 🟡 Partial | `backend/app/core/config.py`, `backend/app/core/sanitizer.py`, `backend/.env.example` | Env-based config and redaction exist. No external secret manager or encrypted secret storage exists. |
| Sandbox | 🟡 Partial | `backend/app/analysis/static_tools.py`, `backend/app/analysis/safety.py` | Tools run without shell interpolation and sensitive files are excluded. No container/process sandbox for untrusted repo execution exists. |
| Audit Logs | 🟡 Partial | `backend/app/core/audit.py` | In-memory sanitized audit logger exists. No persistent append-only audit table/store exists. |
| CORS | ✅ Implemented | `backend/app/core/config.py`, `backend/app/main.py` | Explicit localhost defaults exist, and production rejects wildcard origins. |
| CSRF | ❌ Missing | `backend/app/services/auth_service.py` | OAuth `state` can be sent to GitHub but is not validated on callback. |
| Structured Validation | ✅ Implemented | `backend/app/schemas/*.py`, `backend/app/ai/structured.py` | Pydantic request/response schemas and structured-output validation exist. |

---

## Backend

| Feature | Status | Location | Notes |
|---|---:|---|---|
| FastAPI | ✅ Implemented | `backend/app/main.py`, `backend/app/api/v1/router.py` | Versioned FastAPI application and routers exist. |
| SQLAlchemy | ✅ Implemented | `backend/app/db/session.py`, `backend/app/models/*.py` | Async SQLAlchemy models and session factory exist. |
| Alembic | ✅ Implemented | `backend/alembic/env.py`, `backend/alembic/versions/20260727_0001_backend_foundation.py` | Migration environment and initial schema exist. |
| Redis | 🟡 Partial | `backend/app/analysis/summarizer.py`, `backend/app/workers/celery_app.py`, `backend/app/core/config.py` | Redis is configured for Celery and repository summary cache. No durable app-wide state/cache abstraction exists. |
| Celery | 🟡 Partial | `backend/app/workers/celery_app.py`, `backend/app/workers/tasks.py` | Worker queues and retry/dead-letter behavior exist. Main run task is a placeholder. |
| WebSockets | 🟡 Partial | `backend/app/api/v1/routers/ws.py`, `backend/app/services/websocket_manager.py` | Authenticated WebSocket endpoint and manager exist. No producer broadcasts from execution pipeline. |
| Dependency Injection | ✅ Implemented | `backend/app/api/dependencies.py` | DB session and service dependencies are provided through FastAPI. |
| Repository Pattern | ✅ Implemented | `backend/app/repositories/*.py` | Base and entity-specific repositories exist. |
| Service Layer | ✅ Implemented | `backend/app/services/*.py` | Auth, repository, run, webhook, and WebSocket services exist. Some services remain shallow. |
| Background Workers | 🟡 Partial | `backend/app/workers/*.py` | Celery worker exists, but autonomous orchestration is not implemented. |
| OpenAPI | ✅ Implemented | `backend/app/main.py` | FastAPI OpenAPI, docs, and redoc routes are configured under `/api/v1`. |
| Health Checks | ✅ Implemented | `backend/app/api/v1/routers/health.py`, `docker-compose.yml` | Process and DB health endpoints exist; Compose backend healthcheck uses `/api/v1/health`. |

---

## Frontend

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Next.js | ✅ Implemented | `frontend/package.json`, `frontend/src/app/layout.tsx`, `frontend/src/app/page.tsx` | Next.js app router project exists. |
| Tailwind | ✅ Implemented | `frontend/src/app/globals.css`, `frontend/postcss.config.mjs` | Tailwind CSS is configured and used. |
| TypeScript | ✅ Implemented | `frontend/tsconfig.json`, `frontend/src/**/*.ts*` | Strict TypeScript config and typed app files exist. |
| React Query | 🟡 Partial | `frontend/src/providers/QueryProvider.tsx`, `frontend/src/components/analytics/AnalyticsPanel.tsx` | Provider exists; only telemetry panel uses a query. |
| Zustand | ✅ Implemented | `frontend/src/store/useAuthStore.ts`, `frontend/src/store/useRepoStore.ts` | Auth and repository UI state stores exist. |
| Dark Mode | ✅ Implemented | `frontend/src/app/layout.tsx`, `frontend/src/app/globals.css` | Dark theme is hard-coded via `className="dark"` and dark CSS palette. |
| Responsive Design | 🟡 Partial | `frontend/src/components/**/*.tsx` | Responsive Tailwind classes exist. No visual regression or responsive tests exist. |
| Execution Timeline | ❌ Missing | `frontend/src/store/useRepoStore.ts`, `frontend/src/components/layout/Navbar.tsx` | Tab label exists, but no timeline view renders. |
| Architecture View | ❌ Missing | `frontend/src/store/useRepoStore.ts`, `frontend/src/components/layout/Navbar.tsx` | Tab label exists, but no architecture view renders. |
| Security Dashboard | ❌ Missing | `frontend/src/components/layout/Navbar.tsx` | Reviews/security tab label exists, but no security dashboard renders. |
| Cost Dashboard | 🟡 Partial | `frontend/src/components/analytics/AnalyticsPanel.tsx` | Cost UI exists but backend telemetry values are hard-coded and frontend has fallback mock data. |
| Provider Dashboard | 🟡 Partial | `frontend/src/components/analytics/AnalyticsPanel.tsx` | Provider health UI exists but data is hard-coded/mock. |
| Notifications | ❌ Missing | `backend/app/models/notification.py` | Backend model exists, but no frontend notifications UI or delivery integration exists. |

---

## DevOps

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Docker | 🟡 Partial | `backend/Dockerfile`, `backend/Dockerfile.worker`, `frontend/Dockerfile` | Dockerfiles exist. Frontend Dockerfile expects `.next/standalone`, but `next.config.ts` does not enable standalone output. |
| Docker Compose | 🟡 Partial | `docker-compose.yml` | Local Postgres, Redis, backend, worker, frontend, and nginx are defined. Credentials are local-dev values and volumes/secrets are absent. |
| GitHub Actions | 🟡 Partial | `.github/workflows/ci-cd.yml` | CI workflow exists. Repository root is not itself a Git repo in the current workspace, while `frontend/` is nested Git metadata. |
| CI/CD | 🟡 Partial | `.github/workflows/ci-cd.yml` | Lint, type-check, tests, security scan, and Docker build jobs exist. No deployment job exists. |
| Health Checks | ✅ Implemented | `docker-compose.yml`, `backend/app/api/v1/routers/health.py` | Backend, Postgres, and Redis health checks exist in Compose; backend exposes process and DB health endpoints. |
| Nginx | ✅ Implemented | `nginx/nginx.conf` | Reverse proxy routes REST, WebSocket, and frontend traffic. |
| `.env.example` | ✅ Implemented | `backend/.env.example`, `frontend/.env.example` | Backend and frontend examples exist and use current backend secret names. No root env example exists. |
| Production Deployment | 🟡 Partial | `DEPLOYMENT_RUNBOOK.md`, `docker-compose.yml`, `.github/workflows/ci-cd.yml` | Runbook and local orchestration exist. Production secrets, migrations, monitoring stack, and deployment target are not implemented. |

---

## Observability

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Logging | ❌ Missing | N/A | No structured logging setup is implemented. |
| OpenTelemetry | ❌ Missing | `frontend/src/components/analytics/AnalyticsPanel.tsx` | UI text mentions OpenTelemetry, but no OpenTelemetry dependency or instrumentation exists. |
| Prometheus | 🟡 Partial | `backend/app/core/metrics.py`, `backend/app/api/v1/endpoints/metrics.py` | Metrics are defined and exported, but request/agent/provider instrumentation is not wired. |
| Grafana | ❌ Missing | N/A | No Grafana config or dashboard exists. |
| Logfire | ❌ Missing | N/A | No Logfire dependency/config exists. |
| Token Usage | 🟡 Partial | `backend/app/ai/schemas.py`, `backend/app/ai/budget.py`, `backend/app/core/metrics.py` | Token usage schema and budget accounting exist. Metrics are not wired into provider calls. |
| Provider Metrics | 🟡 Partial | `backend/app/core/metrics.py`, `backend/app/api/v1/endpoints/metrics.py` | Provider metric definitions exist; telemetry endpoint returns hard-coded provider values. |
| Latency | 🟡 Partial | `backend/app/ai/benchmarking.py`, `backend/app/api/v1/endpoints/metrics.py` | Benchmark latency is measured in tests; telemetry endpoint uses hard-coded latencies. |
| Retry Statistics | ❌ Missing | N/A | Retry policy exists, but no retry statistics are recorded or exported. |
| Execution Replay | ❌ Missing | N/A | No execution replay storage or API exists. |
| Guardrail Logs | ❌ Missing | `backend/app/core/metrics.py` | Guardrail counter exists, but no guardrail log/event pipeline exists. |

---

## Testing

| Feature | Status | Location | Notes |
|---|---:|---|---|
| Unit Tests | ✅ Implemented | `backend/tests/*.py` | Backend unit tests exist for auth, AI abstractions, analysis helpers, security helpers, and workers. |
| Integration Tests | 🟡 Partial | `backend/tests/test_webhooks.py`, `backend/tests/test_api_routes.py` | API/webhook flows are tested with SQLite and mocks. No external services or full stack integration tests exist. |
| API Tests | ✅ Implemented | `backend/tests/test_api_routes.py`, `backend/tests/test_api_auth.py`, `backend/tests/test_webhooks.py`, `backend/tests/test_observability_and_security.py` | Backend route tests exist. |
| Frontend Tests | ❌ Missing | N/A | No frontend test framework, component tests, or E2E tests exist. |
| LangGraph Tests | 🟡 Partial | `backend/tests/test_agent_foundation.py` | Skeleton graph execution is tested. Real agent behavior is not tested. |
| Provider Tests | 🟡 Partial | `backend/tests/test_ai_provider_abstraction.py` | Mock provider fallback/retry/budget behavior is tested. Real HTTP provider behavior is not fully covered. |
| Golden Test Cases | ✅ Implemented | `backend/tests/golden/golden_repo_v1.json`, `backend/tests/test_golden_regression.py` | One golden fixture and regression test exist. |
| Provider Benchmarking | 🟡 Partial | `backend/app/ai/benchmarking.py`, `backend/tests/test_golden_regression.py` | Benchmark engine exists and is tested with a mock provider. |
| Coverage | ❌ Missing | N/A | No coverage configuration, thresholds, or CI coverage artifact exists. |

---

## Deferred Features

| Feature | Reason Deferred | Planned Version |
|---|---|---|
| Persistent user identity flows | `AuthService.exchange_github_code()` comments that user persistence is intentionally minimal until identity flows mature. | Phase 3 |
| Autonomous run orchestration entrypoint | `enqueue_run()` is explicitly documented as a placeholder for Phase 3/4 orchestration. | Phase 3/4 |
| Tree-sitter grammar-backed parsing | `TreeSitterAstService` records parse targets and comments that installed grammars can be added by future agent tools. | Phase 4 |
| Durable AI retry queue | `InMemoryRetryQueue` is documented as a minimal Phase 3 test abstraction. | Phase 3 |

---

## Missing Features

| Feature | Recommendation | Priority |
|---|---|---:|
| Embedding provider abstraction and implementations | Add a dedicated embedding interface, provider implementations, dimension checks, batching, and caching before any vector/RAG workflow is claimed. | High |
| Backend repository connection endpoint | Implement or remove frontend `connectRepository()` and local connect modal behavior as production paths. | High |
| Backend manual run trigger endpoint | Implement or remove frontend `triggerRun()` API helper and Launch Run UI path. | High |
| Real LangGraph agent execution | Replace placeholder nodes with prompt/provider/tool execution and persist outputs/events. | High |
| Deployment Validator agent | Add graph node, prompt/service, and tests or remove the permission entry until implemented. | Medium |
| Memory Manager agent | Add graph node, durable memory storage, and tests or remove the permission entry until implemented. | Medium |
| LangGraph checkpointing | Add a supported checkpointer and persistence strategy before claiming resumable agent execution. | High |
| Execution replay | Persist graph states/events and expose replay API/UI. | Medium |
| OAuth state validation / CSRF protection | Store and validate OAuth state on callback. | High |
| Tenant-scoped authorization | Enforce organization/repository membership in repository and run queries. | High |
| Frontend execution timeline view | Implement a run timeline view backed by API/WebSocket events. | Medium |
| Frontend architecture/security/review views | Implement the currently empty dashboard tabs or remove them from navigation. | Medium |
| Frontend tests | Add component tests and at least one E2E smoke path. | Medium |
| Observability instrumentation | Wire request, provider, agent, retry, and guardrail metrics to actual execution paths. | Medium |
| Production sandbox | Run untrusted repository analysis in a constrained workspace/container with resource limits. | High |
| Persistent audit log | Store audit records in the database or append-only external sink. | Medium |
| Production deployment target | Add documented deployment target, secrets, migrations, and monitoring stack. | Medium |

---

## Project Statistics

| Metric | Value | Method |
|---|---:|---|
| Number of Python files | 100 | Counted under `backend/app`, `backend/tests`, and `backend/alembic`. |
| Number of TypeScript / TSX files | 16 | Counted project-owned `frontend/**/*.ts` and `frontend/**/*.tsx`, excluding generated folders. |
| Number of React components / exported app functions | 10 | Counted exported functions in `frontend/src`. |
| Number of API routes | 10 | Counted `@router.get`, `@router.post`, and `@router.websocket` declarations in `backend/app/api`. |
| Number of LangGraph nodes | 9 | Counted `builder.add_node(...)` calls in `backend/app/agents/graph.py`. |
| Number of concrete AI chat providers | 4 | Gemini, OpenAI, Groq, and Ollama provider classes. |
| Number of test functions | 51 | Counted `def test_*` and `async def test_*` in `backend/tests`. |
| Number of backend test files | 9 | Counted `backend/tests/test_*.py`. |
| Number of Docker files | 3 | `backend/Dockerfile`, `backend/Dockerfile.worker`, `frontend/Dockerfile`. |
| Number of GitHub Actions workflows | 1 | Counted workflow files in `.github/workflows`. |
| Number of database model classes | 13 | Counted SQLAlchemy model classes inheriting from `Base` in `backend/app/models`. |

---

## Overall Completion

| Area | Completion | Justification |
|---|---:|---|
| Core Platform | 35% | Data models, API foundations, prompts, and skeleton graph exist, but repository connection, run execution, agent outputs, PR generation, timeline, and most dashboard flows are incomplete or mock-only. |
| AI Layer | 60% | Chat provider abstraction, concrete providers, fallback, retry, structured output, budget, key rotation, and tests exist. Embeddings are absent, provider state is in-memory, costs are mostly stubbed, and AI is not wired into agents. |
| Frontend | 35% | Next.js/Tailwind/TypeScript shell is present with a good dashboard surface, but repository, auth, run, timeline, graph, review, and architecture workflows are mostly mock or empty. |
| Backend | 70% | FastAPI, SQLAlchemy, Alembic, repositories, services, Celery config, Redis config, WebSockets, health checks, and tests exist. Core orchestration and several write endpoints are not implemented. |
| Security | 55% | JWT, route guards, webhook HMAC, CORS hardening, rate limiting, WebSocket auth, sanitizer, and validation exist. OAuth CSRF, tenant-scoped RBAC, durable audit, sandboxing, and external secrets management are missing. |
| Testing | 50% | Backend unit/API/provider-foundation tests are substantial. There are no frontend, E2E, real provider, real Celery/Redis, PostgreSQL migration, or coverage-threshold tests. |
| Observability | 25% | Prometheus endpoint and metric definitions exist, plus a mock telemetry dashboard. Metrics are not wired into real request/provider/agent execution, and OpenTelemetry/Grafana/Logfire are missing. |
| DevOps | 50% | Dockerfiles, Docker Compose, nginx, CI workflow, env examples, and runbook exist. Production deployment, migrations, secrets, volumes, monitoring, image scanning, and frontend standalone Docker alignment are incomplete. |
| Overall | 48% | The repository is a credible backend foundation and demo UI, but the autonomous workflow, embedding layer, production observability, frontend integration, and several security/DevOps requirements remain incomplete. |
