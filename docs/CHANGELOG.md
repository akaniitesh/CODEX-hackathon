# Changelog

All notable changes to the **Autonomous Software Engineering Platform** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- **Persistent User Identity**: Mature user identity persistence and OAuth state CSRF validation.
- **Autonomous Orchestration Entrypoint**: Transition `enqueue_run()` into background agent run execution loop.
- **Tree-sitter Grammar Parsing**: Extend `TreeSitterAstService` with installed grammars for multi-language AST extraction.
- **Durable Redis Retry Queue**: Upgrade `InMemoryRetryQueue` to a persistent Redis-backed retry queue.

---

## [0.2.0] - 2026-07-28

### Added
- **Gemini AI Provider**: Integrated `GeminiProvider` as the fourth concrete implementation of `BaseAIProvider` (via `HttpChatProvider`), utilizing Google's OpenAI-compatible REST API (`/v1beta/openai`).
- **Gemini Settings & Environment Variables**: Added `GOOGLE_API_KEY`, `MODEL_NAME` (`gemini-1.5-flash`), `gemini_api_keys`, and `gemini_base_url` to `Settings` ([config.py](file:///d:/Codex%20Hackathon/backend/app/core/config.py)) and `backend/.env.example`.
- **Gemini Unit Tests**: Added provider factory and fallback chain unit tests verifying `AI_PROVIDER=gemini` selection and provider ordering ([test_ai_provider_abstraction.py](file:///d:/Codex%20Hackathon/backend/tests/test_ai_provider_abstraction.py)).
- **Documentation Suite**: Created comprehensive documentation suite:
  - `README.md`: Flagship project documentation with Mermaid architecture diagrams.
  - `INSTALLATION_GUIDE.md`: Step-by-step Windows setup guide.
  - `DEVELOPER_GUIDE.md`: Architectural reference and contribution tutorial.
  - `ARCHITECTURE.md`: High-level system architecture blueprint and ER diagrams.
  - `API_REFERENCE.md`: Complete OpenAPI endpoint and WebSocket specification.
  - `TROUBLESHOOTING.md`: 21-issue searchable diagnostic guide.
  - `CONTRIBUTING.md`: Git branching, coding standards, and PR guidelines.

### Changed
- **Resilient Fallback Chain Order**: Updated `create_fallback_provider()` chain sequence in `AIProviderFactory` ([factory.py](file:///d:/Codex%20Hackathon/backend/app/ai/factory.py)) to:
  $$\text{Gemini} \longrightarrow \text{OpenAI} \longrightarrow \text{Groq} \longrightarrow \text{Ollama} \longrightarrow \text{Retry Queue}$$
- **Provider Enum**: Expanded `ProviderName` enum ([schemas.py](file:///d:/Codex%20Hackathon/backend/app/ai/schemas.py)) to include `GEMINI = "gemini"`.

### Fixed
- Fixed API key rotation validator in `Settings` to parse comma-separated `gemini_api_keys`.

### Security
- Re-verified secret sanitizer regex filtering across Gemini API keys and Bearer JWT tokens.

---

## [0.1.0] - 2026-07-27

### Added
- **Core FastAPI Backend**: Initial setup of versioned REST API routers (`/api/v1`), async SQLAlchemy ORM models, and Alembic migrations.
- **AI Provider Abstraction Layer**: Implemented `BaseAIProvider`, `HttpChatProvider`, `OpenAIProvider`, `GroqProvider`, `OllamaProvider`, `FallbackAIProvider`, 3-state `CircuitBreaker`, `ApiKeyRing`, and `TokenBudgetManager`.
- **LangGraph State Engine**: Initialized 9-node `StateGraph` skeleton (`AutonomousAgentState`), versioned `PromptRegistry`, and `ToolPermissionManager`.
- **Repository Analysis Services**: Built `DirectoryTreeService`, `ReadmeService`, `TreeSitterAstService`, `ImportGraphService`, `GitHistoryService`, static tool wrappers (Ruff, Bandit, Semgrep, Radon), and SHA-keyed `RepositorySummarizer` with Redis caching.
- **Next.js 16 Frontend**: App Router dashboard shell, dark mode palette, repository list grid, Zustand state stores, and telemetry panel.
- **Security & Hardening**: Implemented JWT authentication, GitHub OAuth start/callback routes, GitHub Webhook HMAC SHA256 verification, token bucket `RateLimiter`, security headers middleware, and `AuditLogger`.
- **DevOps & CI/CD**: Created Dockerfiles, `docker-compose.yml`, Nginx reverse proxy config, and 6-stage GitHub Actions workflow.
