# Production Deployment & Operations Runbook

## Overview
This runbook describes the deployment, configuration, local orchestration, and telemetry monitoring for **Aegis AI**.

---

## 1. Local Development Setup (Docker Compose)

### Prerequisites
- Docker Engine 24.0+ & Docker Compose 2.20+
- Python 3.11+
- Node.js 20+

### Launching the Platform Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/enterprise-org/autonomous-se-platform.git
   cd autonomous-se-platform
   ```

2. Copy environment variable templates:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. Launch all services via Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

4. Verify service health endpoints:
   - **Frontend App**: `http://localhost`
   - **Backend REST API**: `http://localhost/api/v1/health`
   - **Prometheus Metrics**: `http://localhost/api/v1/metrics/prometheus`
   - **Telemetry Health**: `http://localhost/api/v1/telemetry/health`
     - Requires an admin JWT in the `Authorization` header.

---

## 2. Automated CI/CD Pipeline (GitHub Actions)

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) enforces 6 mandatory quality gates on every Pull Request and main push:

1. **Linting**: Runs `ruff check` on Python and `npm run lint` on Next.js.
2. **Type Checking**: Runs `mypy app tests` (`strict = true`) and `npm run build` (TypeScript compiler).
3. **Automated Tests**: Runs the Pytest suite with mock AI providers.
4. **Golden Regression Check**: Executes `pytest tests/test_golden_regression.py` against golden fixtures.
5. **Security & Vulnerability Scan**: Scans AST with `bandit` and node dependencies with `npm audit`.
6. **Container Build Verification**: Builds multi-stage Docker images for backend, worker, and frontend.

---

## 3. Security Hardening & Secret Management

- **Zero Secret Leakage**: All API keys, JWT tokens, OAuth client secrets, and passwords are sanitized via `SecretSanitizer` before reaching logs or LLM context windows.
- **Production Secrets**: Use AWS Secrets Manager, HashiCorp Vault, or GCP Secret Manager in production. Never check `.env` files into source control.
- **Required Secret Names**: Configure `JWT_SECRET_KEY` and `GITHUB_WEBHOOK_SECRET`.
  Legacy `SECRET_KEY` and `WEBHOOK_SECRET` are still accepted for compatibility.
- **CORS**: Configure explicit `CORS_ORIGINS`; wildcard origins are rejected in production.
- **Rate Limiting**: API routes are rate-limited via sliding window token bucket (`RateLimiter`) wired through middleware.
- **Security Headers**: Enforced via `SecurityHeadersMiddleware` (`nosniff`, `DENY`, `1; mode=block`, `HSTS`).
- **Protected Realtime & Telemetry**: Prometheus and telemetry endpoints require an admin JWT. Run WebSocket subscriptions require a valid JWT via `?token=` or bearer header.

---

## 4. Telemetry & Monitoring

- **Prometheus**: Exposed at `/api/v1/metrics/prometheus`.
- **Telemetry Dashboard**: Exposed at `/api/v1/telemetry/health` and rendered dynamically in the frontend **Cost & Model Health** panel.
- **Circuit Breakers**: Live status monitored across Gemini, OpenAI, Groq, and Ollama providers with automatic cooldown probes.

---

## 5. Frontend Production Deployment (Vercel)

The Next.js frontend is deployed live on Vercel:
- **Production Dashboard**: [https://aegisai-autonomous-sep.vercel.app](https://aegisai-autonomous-sep.vercel.app)
- **Deployment URL**: [https://frontend-lgqd6yilk-akaniiteshs-projects.vercel.app](https://frontend-lgqd6yilk-akaniiteshs-projects.vercel.app)

### Local CLI Deployments
Any subsequent updates can be deployed directly from the `frontend/` directory if you have an active session logged in:
```bash
cd frontend
# Deploy preview
npx vercel
# Deploy production
npx vercel --prod
```

