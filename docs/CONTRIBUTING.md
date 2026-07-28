# Autonomous Software Engineering Platform: Contributing Guide

Thank you for your interest in contributing to the **Autonomous Software Engineering Platform**! This document provides guidelines and instructions for submitting contributions to this codebase.

---

## Table of Contents

1. [Code of Conduct & Principles](#1-code-of-conduct--principles)
2. [Local Environment Setup](#2-local-environment-setup)
3. [Git Branching Strategy](#3-git-branching-strategy)
4. [Coding Standards](#4-coding-standards)
5. [Formatting & Linting](#5-formatting--linting)
6. [Testing Requirements](#6-testing-requirements)
7. [Commit Message Conventions](#7-commit-message-conventions)
8. [Pull Request Lifecycle & Review Checklist](#8-pull-request-lifecycle--review-checklist)
9. [Extension Walkthroughs](#9-extension-walkthroughs)
   - [A. Adding a New API Endpoint](#a-adding-a-new-api-endpoint)
   - [B. Adding a New LangGraph Node](#b-adding-a-new-langgraph-node)
   - [C. Adding a New LLM Provider](#c-adding-a-new-llm-provider)
   - [D. Adding a New Embedding Provider](#d-adding-a-new-embedding-provider)
   - [E. Adding a New Frontend Page](#e-adding-a-new-frontend-page)
10. [Code Review Expectations](#10-code-review-expectations)

---

# 1. Code of Conduct & Principles

- **Safety & Isolation**: Never execute untrusted code without process isolation. Sanitize all secrets and API keys before logging or persisting events.
- **Design Before Code**: For non-trivial modifications, propose an architectural outline in an issue or PR description before writing implementation logic.
- **Strict Verification**: Code edits are not complete until linting (`ruff check`), type checking (`mypy strict`), and unit tests (`pytest`) pass 100%.

---

# 2. Local Environment Setup

Follow these steps to set up your local development workspace:

```bash
# 1. Clone the repository
git clone https://github.com/enterprise-org/autonomous-se-platform.git
cd autonomous-se-platform

# 2. Setup Backend Python Virtual Environment
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -e .[dev]
cp .env.example .env

# 3. Setup Frontend Node Environment
cd ../frontend
npm install
cp .env.example .env.local
```

---

# 3. Git Branching Strategy

We enforce a structured Git branching workflow:

- `main`: Production-ready, highly stable code.
- `dev`: Primary integration branch for upcoming releases.
- `feature/<short-description>`: New capabilities or architectural extensions (e.g. `feature/gemini-embedding-provider`).
- `fix/<short-description>`: Bug fixes and security patches (e.g. `fix/jwt-expiration-handling`).
- `docs/<short-description>`: Documentation additions and clarifications.

---

# 4. Coding Standards

### Python Standards
- Target runtime: **Python 3.11+**.
- Type Hints: 100% type annotations required across all functions. Checked with `mypy --strict`.
- Async I/O: Use `async/await` for database queries (`asyncpg`), HTTP calls (`httpx`), and file I/O.
- Exception Handling: Raise specific domain exceptions (`ApiError`, `ProviderTimeoutError`) instead of catching raw `Exception`.

### TypeScript & React Standards
- Target framework: **Next.js 16 App Router** + **React 19**.
- Type Safety: Enable `strict: true` in `tsconfig.json`. Avoid `any`.
- Styling: Use Tailwind CSS utility classes adhering to the custom dark mode palette (`dark` default).

---

# 5. Formatting & Linting

Before pushing code, format and lint all files:

```bash
# Python Formatting & Linting (Backend)
cd backend
ruff format app tests
ruff check app tests

# Static Type Check
mypy app tests

# TypeScript & Next.js Linting (Frontend)
cd ../frontend
npm run lint
```

---

# 6. Testing Requirements

All contributions must include automated test coverage:

- **Backend Pytest**: Unit and integration tests in `backend/tests/`.
- **Golden Regression Suite**: Ensure prompts and AI output formats do not regress.

```bash
# Run backend test suite
cd backend
pytest -v

# Run golden regression suite
pytest tests/test_golden_regression.py -v
```

---

# 7. Commit Message Conventions

We enforce [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

[optional body]
```

### Supported Types
- `feat`: A new user-facing feature or API capability.
- `fix`: A bug fix in API, agent, or worker code.
- `docs`: Documentation updates.
- `test`: Adding or refactoring unit/integration tests.
- `refactor`: Code restructuring without functional changes.
- `ci`: CI/CD workflow updates.

### Examples
```bash
git commit -m "feat(ai): add GeminiProvider to AIProviderFactory and fallback chain"
git commit -m "fix(auth): sanitize JWT bearer tokens before logging exception traces"
```

---

# 8. Pull Request Lifecycle & Review Checklist

1. **Create Topic Branch**: Branch off `dev`.
2. **Implement & Test**: Write clean code and accompanying Pytest tests.
3. **Verify Locally**: Ensure `ruff`, `mypy`, and `pytest` pass cleanly.
4. **Submit PR**: Open a Pull Request targeting `dev` with a clear description of changes.
5. **CI Automation**: Confirm all 6 GitHub Actions CI quality gates pass.

### PR Review Checklist
- [ ] Code follows project architecture and layer isolation.
- [ ] No secrets or API keys are logged or hardcoded.
- [ ] Type hints are complete (`mypy` zero errors).
- [ ] Pytest test cases cover new branches and failure paths.
- [ ] Documentation updated if APIs or configuration options changed.

---

# 9. Extension Walkthroughs

### A. Adding a New API Endpoint
1. Add request/response Pydantic models in `backend/app/schemas/`.
2. Implement router logic in `backend/app/api/v1/routers/`.
3. Register router in `backend/app/api/v1/router.py`.
4. Add route test in `backend/tests/test_api_routes.py`.

### B. Adding a New LangGraph Node
1. Define state additions in `AutonomousAgentState` ([schemas.py](file:///d:/Codex%20Hackathon/backend/app/agents/schemas.py)).
2. Add agent prompt template under `backend/app/agents/prompts/templates/`.
3. Declare tool permissions in `AGENT_TOOL_ALLOWLIST` ([permissions.py](file:///d:/Codex%20Hackathon/backend/app/agents/permissions.py)).
4. Add node execution step function and link in `build_graph_skeleton()` ([graph.py](file:///d:/Codex%20Hackathon/backend/app/agents/graph.py)).

### C. Adding a New LLM Provider
1. Add enum entry in `ProviderName` ([schemas.py](file:///d:/Codex%20Hackathon/backend/app/ai/schemas.py)).
2. Implement provider class inheriting `HttpChatProvider` in `app/ai/providers.py`.
3. Register provider mapping in `_provider_map()` ([factory.py](file:///d:/Codex%20Hackathon/backend/app/ai/factory.py)).

### D. Adding a New Embedding Provider
1. Declare embedding interface `BaseEmbeddingProvider`.
2. Implement provider class (`embed_documents`, `embed_query`, `dimension`).
3. Register provider in `EmbeddingProviderFactory`.

### E. Adding a New Frontend Page
1. Add route page in `frontend/src/app/<route-name>/page.tsx`.
2. Create reusable UI components in `frontend/src/components/`.
3. Connect state via Zustand store (`useRepoStore`).

---

# 10. Code Review Expectations

- **Response Time**: Maintainers strive to review PRs within 48 hours.
- **Constructive Feedback**: Reviews focus on technical correctness, safety, performance, and readability.
- **Approval Requirements**: At least one maintainer approval is required before merging into `dev`.
