# Backend Foundation

Phase 2 establishes the async FastAPI backend for the autonomous software
engineering platform. Routes are versioned under `/api/v1`, routers stay thin,
and persistence goes through service and repository layers.

## Run locally

```powershell
cd backend
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
```

Start a worker separately:

```powershell
celery -A app.workers.celery_app.celery_app worker -Q runs,dead_letter --loglevel=info
```

## Phase 2 decisions

- GitHub webhook HMAC verification happens before JSON parsing.
- Webhook idempotency checks use `X-GitHub-Delivery` first, then
  repository + commit SHA + event type.
- Notifications are in-app/WebSocket only for v1.
- Repository summaries are cached in Redis and invalidated by commit SHA.
- Static analysis wrappers run deterministic tools with timeouts and without
  shell interpolation.
- Connected repository secrets and key-like files are excluded from analysis
  ingestion.
- `JWT_SECRET_KEY`, `GITHUB_WEBHOOK_SECRET`, and explicit `CORS_ORIGINS` are
  required for production. Legacy `SECRET_KEY`, `WEBHOOK_SECRET`, and `ENV`
  names are still accepted for compatibility.
- Telemetry and Prometheus endpoints require an admin JWT, and run WebSocket
  subscriptions require a valid JWT passed as `?token=` or a bearer header.
