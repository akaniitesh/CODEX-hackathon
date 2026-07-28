# Autonomous Software Engineering Platform: Troubleshooting Guide

> **Target Audience**: This document is a comprehensive, searchable diagnostic guide for resolving operational, setup, database, network, AI provider, container, and security errors across the platform.

---

## Table of Contents

- [1. Python & Virtual Environment Issues](#1-python--virtual-environment-issues)
  - [ISSUE-01: Python Version Mismatch (< 3.11)](#issue-01-python-version-mismatch--311)
  - [ISSUE-02: PowerShell Script Execution Disabled (`Activate.ps1`)](#issue-02-powershell-script-execution-disabled-activateps1)
- [2. Database & Alembic Migration Errors](#2-database--alembic-migration-errors)
  - [ISSUE-03: PostgreSQL Connection Refused (`asyncpg.exceptions.CannotConnectNowError`)](#issue-03-postgresql-connection-refused-asyncpgexceptionscannotconnectnowerror)
  - [ISSUE-04: Invalid Database Driver Prefix (`postgres://` vs `postgresql+asyncpg://`)](#issue-04-invalid-database-driver-prefix-postgres-vs-postgresqlasyncpg)
  - [ISSUE-05: Alembic Migration State Divergence / Head Mismatch](#issue-05-alembic-migration-state-divergence--head-mismatch)
- [3. Redis & Celery Worker Failures](#3-redis--celery-worker-failures)
  - [ISSUE-06: Redis Connection Refused (`redis.exceptions.ConnectionError`)](#issue-06-redis-connection-refused-redisexceptionsconnectionerror)
  - [ISSUE-07: Celery Tasks Hanging or Routed to Dead-Letter Queue](#issue-07-celery-tasks-hanging-or-routed-to-dead-letter-queue)
- [4. AI Provider & Authentication Failures](#4-ai-provider--authentication-failures)
  - [ISSUE-08: Missing API Key for Active Provider (`GOOGLE_API_KEY` / `OPENAI_API_KEY`)](#issue-08-missing-api-key-for-active-provider-google_api_key--openai_api_key)
  - [ISSUE-09: Gemini / OpenAI API Key Invalid or Rate Limited (`429` / `401`)](#issue-09-gemini--openai-api-key-invalid-or-rate-limited-429--401)
  - [ISSUE-10: Circuit Breaker Tripped to OPEN State](#issue-10-circuit-breaker-tripped-to-open-state)
  - [ISSUE-11: Local Ollama Connection Refused (`http://localhost:11434`)](#issue-11-local-ollama-connection-refused-httplocalhost11434)
- [5. Webhook, OAuth & Auth Security Errors](#5-webhook-oauth--auth-security-errors)
  - [ISSUE-12: GitHub Webhook HMAC Signature Verification Failure (`400 Bad Request`)](#issue-12-github-webhook-hmac-signature-verification-failure-400-bad-request)
  - [ISSUE-13: GitHub OAuth Redirect URI Mismatch / Bad Code](#issue-13-github-oauth-redirect-uri-mismatch--bad-code)
  - [ISSUE-14: JWT Decoding Failure / Expired Token (`401 Unauthorized`)](#issue-14-jwt-decoding-failure--expired-token-401-unauthorized)
- [6. Networking, Ports & CORS Issues](#6-networking-ports--cors-issues)
  - [ISSUE-15: Port Conflicts (5432, 6379, 8000, 3000)](#issue-15-port-conflicts-5432-6379-8000-3000)
  - [ISSUE-16: CORS Origin Rejection (`Access-Control-Allow-Origin`)](#issue-16-cors-origin-rejection-access-control-allow-origin)
  - [ISSUE-17: WebSocket Connection Immediate Disconnect (`Close Code 1008`)](#issue-17-websocket-connection-immediate-disconnect-close-code-1008)
- [7. Docker & Container Stack Failures](#7-docker--container-stack-failures)
  - [ISSUE-18: Docker Desktop Engine Not Started](#issue-18-docker-desktop-engine-not-started)
  - [ISSUE-19: Nginx Reverse Proxy Upstream Connection Refused](#issue-19-nginx-reverse-proxy-upstream-connection-refused)
- [8. LangGraph Execution & Guardrail Errors](#8-langgraph-execution--guardrail-errors)
  - [ISSUE-20: Tool Execution Denied (`ToolPermissionDeniedError 403`)](#issue-20-tool-execution-denied-toolpermissiondeniederror-403)
  - [ISSUE-21: Token Budget USD Ceiling Tripped (`TokenBudgetExceededError`)](#issue-21-token-budget-usd-ceiling-tripped-tokenbudgetexceedederror)

---

# 1. Python & Virtual Environment Issues

### ISSUE-01: Python Version Mismatch (< 3.11)

- **Symptoms**: Syntax errors such as `TypeError: unsupported operand type(s) for |` or `ModuleNotFoundError: No module named 'enum.StrEnum'`.
- **Cause**: Python runtime version is older than `3.11`.
- **Solution**: Install Python `3.11` or higher from Python.org.
- **Verification**: Run `python --version` to confirm version `>= 3.11.0`.
- **Commands**:
  ```powershell
  python --version
  ```

---

### ISSUE-02: PowerShell Script Execution Disabled (`Activate.ps1`)

- **Symptoms**: Running `.\.venv\Scripts\Activate.ps1` returns:  
  `File ...\Activate.ps1 cannot be loaded because running scripts is disabled on this system.`
- **Cause**: Windows PowerShell default security policy restricts executing unsigned local scripts.
- **Solution**: Set PowerShell execution policy for the current process to `RemoteSigned`.
- **Verification**: Virtual environment prefix `(.venv)` appears in the PowerShell prompt.
- **Commands**:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\.venv\Scripts\Activate.ps1
  ```

---

# 2. Database & Alembic Migration Errors

### ISSUE-03: PostgreSQL Connection Refused (`asyncpg.exceptions.CannotConnectNowError`)

- **Symptoms**: Backend crash on startup with `ConnectionRefusedError: [Errno 111] Connect call failed ('127.0.0.1', 5432)`.
- **Cause**: PostgreSQL container or local service is not running.
- **Solution**: Start the PostgreSQL container via Docker.
- **Verification**: Run `docker ps` to verify `postgres-db` status is `Up`.
- **Commands**:
  ```powershell
  docker run -d --name postgres-db -e POSTGRES_DB=autose_platform -e POSTGRES_USER=autose_user -e POSTGRES_PASSWORD=autose_password -p 5432:5432 postgres:16-alpine
  ```

---

### ISSUE-04: Invalid Database Driver Prefix (`postgres://` vs `postgresql+asyncpg://`)

- **Symptoms**: SQLAlchemy initialization error: `NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`.
- **Cause**: Connection string starts with `postgres://` or `postgresql://` instead of `postgresql+asyncpg://`.
- **Solution**: Update `DATABASE_URL` in `backend/.env` to use the `postgresql+asyncpg://` dialect.
- **Verification**: Test database connectivity via `GET /api/v1/health/db`.
- **Commands**:
  ```ini
  # In backend/.env
  DATABASE_URL=postgresql+asyncpg://autose_user:autose_password@localhost:5432/autose_platform
  ```

---

### ISSUE-05: Alembic Migration State Divergence / Head Mismatch

- **Symptoms**: `alembic upgrade head` fails with `Can't locate revision identified by '...'`.
- **Cause**: Local database schema is out of sync with migration scripts in `backend/alembic/versions/`.
- **Solution**: Reset migration state or stamp head.
- **Verification**: Run `alembic current` to verify current head matches the latest revision.
- **Commands**:
  ```powershell
  cd backend
  alembic stamp head
  alembic upgrade head
  ```

---

# 3. Redis & Celery Worker Failures

### ISSUE-06: Redis Connection Refused (`redis.exceptions.ConnectionError`)

- **Symptoms**: Celery worker fails with `redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379`.
- **Cause**: Redis server is stopped or unreachable.
- **Solution**: Launch a Redis 7 Alpine container via Docker.
- **Verification**: Run `redis-cli ping` inside container to receive `PONG`.
- **Commands**:
  ```powershell
  docker run -d --name redis-server -p 6379:6379 redis:7-alpine
  docker exec -it redis-server redis-cli ping
  ```

---

### ISSUE-07: Celery Tasks Hanging or Routed to Dead-Letter Queue

- **Symptoms**: Runs remain in `queued` status indefinitely or move straight to `failed`.
- **Cause**: Celery worker process is not listening on the `runs` queue or unhandled exceptions routed to `dead_letter`.
- **Solution**: Ensure worker process is active with explicit queue arguments.
- **Verification**: Check worker console output for `[tasks] . app.workers.tasks.enqueue_run`.
- **Commands**:
  ```powershell
  cd backend
  celery -A app.workers.celery_app worker --loglevel=info -Q runs,dead_letter
  ```

---

# 4. AI Provider & Authentication Failures

### ISSUE-08: Missing API Key for Active Provider (`GOOGLE_API_KEY` / `OPENAI_API_KEY`)

- **Symptoms**: LLM calls fail with `ValueError: No valid API keys provided for ProviderName.GEMINI`.
- **Cause**: `AI_PROVIDER=gemini` is set in `.env`, but `GOOGLE_API_KEY` is empty.
- **Solution**: Provide valid API key in `backend/.env` or switch active provider to `ollama`.
- **Verification**: Run `pytest tests/test_ai_provider_abstraction.py -v`.
- **Commands**:
  ```ini
  # In backend/.env
  AI_PROVIDER=gemini
  GOOGLE_API_KEY=AIzaSyYourActualKeyHere
  ```

---

### ISSUE-09: Gemini / OpenAI API Key Invalid or Rate Limited (`429` / `401`)

- **Symptoms**: AI provider throws `RateLimitError` or `ProviderNetworkError`.
- **Cause**: Provider quotas exceeded or key revoked.
- **Solution**: Add multiple comma-separated keys in `OPENAI_API_KEYS` to enable `ApiKeyRing` key rotation, or rely on `FallbackAIProvider` automatic failover.
- **Verification**: Inspect telemetry state at `GET /api/v1/telemetry/health`.
- **Commands**:
  ```ini
  OPENAI_API_KEYS=sk-key-1,sk-key-2,sk-key-3
  ```

---

### ISSUE-10: Circuit Breaker Tripped to OPEN State

- **Symptoms**: Logs display `CircuitBreakerOpenError: Circuit breaker for gemini is OPEN`.
- **Cause**: Primary provider encountered consecutive failures exceeding `ai_circuit_failure_threshold` (default 3).
- **Solution**: Wait `ai_circuit_cooldown_seconds` (default 30s) for state to enter `HALF_OPEN` probe mode, or inspect provider health.
- **Verification**: Query `GET /api/v1/telemetry/health` to view `providers.gemini.state`.
- **Commands**:
  ```powershell
  curl http://localhost:8000/api/v1/telemetry/health -H "Authorization: Bearer <admin_token>"
  ```

---

### ISSUE-11: Local Ollama Connection Refused (`http://localhost:11434`)

- **Symptoms**: `ProviderNetworkError: Failed to connect to Ollama at http://localhost:11434/v1`.
- **Cause**: `AI_PROVIDER=ollama` configured, but local Ollama service is not running.
- **Solution**: Download and launch Ollama, or run `ollama serve`.
- **Verification**: Run `curl http://localhost:11434/api/tags` to verify local models.
- **Commands**:
  ```bash
  ollama serve
  ollama run llama3.1
  ```

---

# 5. Webhook, OAuth & Auth Security Errors

### ISSUE-12: GitHub Webhook HMAC Signature Verification Failure (`400 Bad Request`)

- **Symptoms**: GitHub Webhook delivery returns `HTTP 400 Bad Request: Invalid webhook signature`.
- **Cause**: `WEBHOOK_SECRET` in `backend/.env` does not match secret configured in GitHub repository settings.
- **Solution**: Synchronize `WEBHOOK_SECRET` across `backend/.env` and GitHub Webhook settings.
- **Verification**: Run `pytest tests/test_webhooks.py -v`.
- **Commands**:
  ```ini
  WEBHOOK_SECRET=your-shared-webhook-secret
  ```

---

### ISSUE-13: GitHub OAuth Redirect URI Mismatch / Bad Code

- **Symptoms**: `POST /api/v1/auth/github/callback` fails with `ApiError: Invalid authorization code`.
- **Cause**: GitHub Client ID / Secret mismatch or redirect URI misconfiguration in GitHub Developer Portal.
- **Solution**: Verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `backend/.env`.
- **Verification**: Test OAuth start endpoint `GET /api/v1/auth/github/start`.

---

### ISSUE-14: JWT Decoding Failure / Expired Token (`401 Unauthorized`)

- **Symptoms**: Requests return `HTTP 401 Unauthorized: Could not validate credentials`.
- **Cause**: Token expired (>60 min) or `SECRET_KEY` changed.
- **Solution**: Re-authenticate via `/api/v1/auth/github/callback` to acquire a fresh JWT.
- **Verification**: Check JWT payload expiration using `jwt.decode()`.

---

# 6. Networking, Ports & CORS Issues

### ISSUE-15: Port Conflicts (5432, 6379, 8000, 3000)

- **Symptoms**: `OSError: [Errno 10048] address already in use`.
- **Cause**: Another service (local Postgres, Redis, or Node process) is occupying the target port.
- **Solution**: Identify and kill process occupying the port on Windows.
- **Verification**: Confirm port is free.
- **Commands**:
  ```powershell
  # Find process on port 8000
  Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
  ```

---

### ISSUE-16: CORS Origin Rejection (`Access-Control-Allow-Origin`)

- **Symptoms**: Browser console reports:  
  `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy.`
- **Cause**: Frontend origin is missing from `CORS_ORIGINS` in `backend/.env`.
- **Solution**: Update `CORS_ORIGINS` to allow frontend domain.
- **Verification**: Confirm preflight `OPTIONS` request returns `200 OK`.
- **Commands**:
  ```ini
  CORS_ORIGINS=http://localhost:3000,http://localhost
  ```

---

### ISSUE-17: WebSocket Connection Immediate Disconnect (`Close Code 1008`)

- **Symptoms**: WebSocket connection to `WS /api/v1/ws/runs/{run_id}` closes immediately with status code `1008`.
- **Cause**: Missing or invalid `token` query parameter or `Authorization` header.
- **Solution**: Pass valid JWT in query string `?token=<access_token>`.
- **Verification**: Run `pytest tests/test_workers_and_ws.py -v`.

---

# 7. Docker & Container Stack Failures

### ISSUE-18: Docker Desktop Engine Not Started

- **Symptoms**: `docker-compose up` returns `error during connect: Get "http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.24/containers/json": open //./pipe/docker_engine: The system cannot find the file specified.`
- **Cause**: Docker Desktop application is not running on Windows.
- **Solution**: Start Docker Desktop from the Windows Start menu and wait for engine indicator to turn green.
- **Verification**: Run `docker info`.

---

### ISSUE-19: Nginx Reverse Proxy Upstream Connection Refused

- **Symptoms**: Navigating to `http://localhost` returns `502 Bad Gateway`.
- **Cause**: FastAPI backend container (`backend:8000`) or Next.js container (`frontend:3000`) is still starting or unhealthy.
- **Solution**: Check container health statuses.
- **Verification**: Run `docker-compose ps` to ensure all 6 services are `healthy`.
- **Commands**:
  ```powershell
  docker-compose ps
  docker-compose logs -f backend
  ```

---

# 8. LangGraph Execution & Guardrail Errors

### ISSUE-20: Tool Execution Denied (`ToolPermissionDeniedError 403`)

- **Symptoms**: Agent fails step execution with `ToolPermissionDeniedError: Agent 'code_reviewer' is not permitted to execute tool 'delete_file'`.
- **Cause**: Attempted tool invocation is not present in `AGENT_TOOL_ALLOWLIST` ([permissions.py](file:///d:/Codex%20Hackathon/backend/app/agents/permissions.py)).
- **Solution**: Update declarative allowlist in `permissions.py` if tool authorization is intended.
- **Verification**: Run `pytest tests/test_agent_foundation.py -v`.

---

### ISSUE-21: Token Budget USD Ceiling Tripped (`TokenBudgetExceededError`)

- **Symptoms**: AI call throws `TokenBudgetExceededError: Run token budget exceeded ceiling`.
- **Cause**: Execution run exceeded default cost ceiling `ai_run_cost_limit_usd` ($10.00) or token limit `ai_run_token_limit` (100,000 tokens).
- **Solution**: Adjust ceiling thresholds in `backend/.env` for larger repositories.
- **Verification**: Check cost limits in `backend/app/core/config.py`.
- **Commands**:
  ```ini
  AI_RUN_TOKEN_LIMIT=200000
  AI_RUN_COST_LIMIT_USD=25.0
  ```
