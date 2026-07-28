# Enterprise Autonomous Software Engineering Platform: Installation Guide

> **Target Audience**: This guide provides step-by-step instructions for installing, configuring, running, and troubleshooting the platform on a fresh Windows laptop (or macOS/Linux workstation), assuming zero prior familiarity with the codebase.

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [System Requirements](#2-system-requirements)
3. [Software Required](#3-software-required)
4. [Installing Required Software](#4-installing-required-software)
5. [Clone Repository](#5-clone-repository)
6. [Project Folder Structure](#6-project-folder-structure)
7. [Python Environment](#7-python-environment)
8. [Frontend Setup](#8-frontend-setup)
9. [Backend Setup](#9-backend-setup)
10. [Redis Setup](#10-redis-setup)
11. [PostgreSQL Setup](#11-postgresql-setup)
12. [Docker Setup](#12-docker-setup)
13. [Environment Variables](#13-environment-variables)
14. [API Keys](#14-api-keys)
15. [Running the Project](#15-running-the-project)
16. [Running with Docker](#16-running-with-docker)
17. [Running without Docker](#17-running-without-docker)
18. [First Login](#18-first-login)
19. [Troubleshooting](#19-troubleshooting)
20. [Frequently Asked Questions](#20-frequently-asked-questions)
21. [Common Commands](#21-common-commands)
22. [Verification Checklist](#22-verification-checklist)

---

# 1. Project Overview

The **Autonomous Software Engineering Platform** is an enterprise-grade, state-orchestrated multi-agent platform designed to automate codebase understanding, architectural analysis, code reviews, static security audits, documentation generation, and Pull Request preparation.

### Architecture Components & How They Interact
- **Frontend Dashboard (Next.js 16)**: Renders the web interface, repository grid, and real-time telemetry panels. Interacts with the backend via REST API (`/api/v1`) and WebSockets (`/api/v1/ws/connect`).
- **Backend Core (FastAPI)**: Serves REST endpoints, validates JWT authentication, verifies GitHub HMAC SHA256 webhook signatures, and enforces rate limiting.
- **Background Worker Queue (Celery)**: Asynchronously processes long-running repository analysis and orchestration tasks off-loaded from the main API thread.
- **State Engine (LangGraph)**: Orchestrates agent nodes (`planner`, `repo_analyzer`, `architecture_agent`, `code_reviewer`, `test_generator`, `security_auditor`, `documentation_agent`, `pr_generator`, `human_approval`).
- **AI Provider Abstraction**: Dynamically routes LLM calls to Google Gemini, OpenAI, Groq, or local Ollama with automatic failover fallback (**Gemini → OpenAI → Groq → Ollama**), circuit breakers, and key rotation.
- **Database (PostgreSQL 16)**: Persists application state, repository metadata, runs, users, memberships, and timeline events via async SQLAlchemy ORM.
- **Cache & Broker (Redis 7)**: Acts as the Celery task broker and caches deterministic repository summaries keyed by commit SHA.

---

# 2. System Requirements

| Metric | Minimum Requirement | Recommended Requirement |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11 (64-bit), macOS 12+, Ubuntu 22.04 LTS | Windows 11 (64-bit with WSL2) |
| **System Memory (RAM)** | 8 GB | 16 GB or higher |
| **Processor (CPU)** | Dual-Core 2.0 GHz (x86_64 / ARM64) | Quad-Core 3.0 GHz or higher |
| **Available Disk Space**| 10 GB free storage | 25 GB free SSD storage |
| **Network Connection** | Broadband Internet (for downloading dependencies & API calls) | High-Speed Stable Connection |
| **Python** | Python `3.11` or higher | Python `3.11.x` |
| **Node.js** | Node.js `v20.x` LTS or higher | Node.js `v20.18.0` LTS |
| **Docker Engine** | Docker Desktop `4.25+` | Docker Desktop `4.30+` |
| **Git** | Git `2.40+` | Git `2.45+` |

---

# 3. Software Required

To develop, run, and test this project on Windows, install the following software:

1. **Git**: Distributed version control system used to download and track the project repository.
2. **Python (3.11+)**: Programming language runtime required to execute the FastAPI backend, Celery workers, and Pytest suite.
3. **Node.js & npm (v20+)**: JavaScript runtime and package manager required to compile and serve the Next.js frontend app.
4. **Docker Desktop**: Container management platform that bundles Docker Engine and Docker Compose for one-click stack execution.
5. **Redis**: In-memory data store used by Celery for message queuing and repository summary caching (provided automatically via Docker Compose).
6. **PostgreSQL**: Relational database engine storing persistent application entities (provided automatically via Docker Compose).
7. **VS Code (Visual Studio Code)**: Recommended IDE for Python and TypeScript code inspection.
   - *Recommended Extensions*: Python (ms-python.python), Pylance, Tailwind CSS IntelliSense, ESLint, Prettier.
8. **GitHub Desktop (Optional)**: GUI client for Git operations.
9. **Postman / Insomnia**: API testing tool for manually calling FastAPI endpoints.
10. **TablePlus / pgAdmin**: Database GUI client for querying PostgreSQL tables directly.

---

# 4. Installing Required Software

### Step 4.1: Download Software Installers
Visit the official download links below:
- **Git for Windows**: [https://git-scm.com/download/win](https://git-scm.com/download/win)
- **Python 3.11**: [https://www.python.org/downloads/release/python-3119/](https://www.python.org/downloads/release/python-3119/)
- **Node.js v20 LTS**: [https://nodejs.org/en/download/](https://nodejs.org/en/download/)
- **Docker Desktop**: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### Step 4.2: Installation Steps on Windows

#### Installing Python 3.11
1. Run `python-3.11.9-amd64.exe`.
2. **IMPORTANT**: Check the box **"Add python.exe to PATH"** at the bottom of the installer window.
3. Click **Install Now** and wait for completion.

#### Installing Node.js v20
1. Run `node-v20.x.x-x64.msi`.
2. Accept the license agreement, leave default installation settings, and click **Next** until **Finish**.

#### Installing Git for Windows
1. Run `Git-2.x.x-64-bit.exe`.
2. Click **Next** accepting default options, ensuring **Git from the command line and also from 3rd-party software** is selected.

#### Installing Docker Desktop
1. Run `Docker Desktop Installer.exe`.
2. Ensure **Use WSL 2 instead of Hyper-V** is selected.
3. Restart your computer when prompted.

### Step 4.3: Verifying Installations
Open Windows PowerShell or Command Prompt (`cmd`) and verify each command:

```powershell
# Verify Git
git --version
# Expected: git version 2.45.2.windows.1

# Verify Python
python --version
# Expected: Python 3.11.9

# Verify Node.js & npm
node -v
# Expected: v20.18.0

npm -v
# Expected: 10.8.2

# Verify Docker
docker --version
# Expected: Docker version 26.1.4, build 5650f9b

docker compose version
# Expected: Docker Compose version v2.27.1
```

---

# 5. Clone Repository

Git allows you to clone (download) the full codebase onto your local machine.

### Command to Clone
Open PowerShell, navigate to your desired workspace directory (e.g., `C:\Projects`), and run:

```powershell
# Navigate to workspace
cd C:\Projects

# Clone the repository
git clone https://github.com/enterprise-org/autonomous-se-platform.git

# Move into project root directory
cd autonomous-se-platform
```

---

# 6. Project Folder Structure

The project repository is structured into isolated backend, frontend, and infrastructure modules:

```
autonomous-se-platform/
├── backend/                  # FastAPI Python backend application
│   ├── alembic/              # PostgreSQL database migration scripts
│   ├── app/                  # Application code
│   │   ├── agents/           # LangGraph state schema, prompt registry, tool allowlists, & state graph
│   │   ├── ai/               # Multi-provider LLM abstraction, factory, circuit breakers, & fallback
│   │   ├── analysis/         # AST target discovery, import graph, static tool wrappers, & summarizer
│   │   ├── api/              # FastAPI REST routers, OpenAPI documentation, & dependencies
│   │   ├── core/             # Configuration, security, secret sanitizer, metrics, & rate limiting
│   │   ├── db/               # Async SQLAlchemy database session factory
│   │   ├── models/           # SQLAlchemy ORM entity models
│   │   ├── repositories/     # Data Access Object repository classes
│   │   ├── schemas/          # Pydantic API validation schemas
│   │   ├── services/         # Application business logic services
│   │   └── workers/          # Celery worker task definitions & dead-letter queue
│   ├── tests/                # Pytest test suite (49 unit, API, & golden regression tests)
│   ├── Dockerfile            # Production Dockerfile for Backend API
│   ├── Dockerfile.worker     # Production Dockerfile for Celery Worker
│   └── pyproject.toml        # Dependencies, Ruff, and MyPy strict configuration
├── frontend/                 # Next.js 16 TypeScript web application
│   ├── src/
│   │   ├── app/              # Next.js App Router layout and pages
│   │   ├── components/       # UI components (AppShell, Navbar, Modals, AnalyticsPanel)
│   │   ├── lib/              # REST API client & domain TypeScript interfaces
│   │   ├── providers/        # React Query provider client
│   │   └── store/            # Zustand global state stores
│   ├── Dockerfile            # Production Dockerfile for Frontend
│   └── package.json          # Node package dependencies
├── nginx/
│   └── nginx.conf            # Reverse proxy configuration routing API and Frontend
├── docker-compose.yml        # Local production orchestration container stack
├── DEPLOYMENT_RUNBOOK.md     # Deployment operations runbook
├── FEATURE_MATRIX.md         # Ground-truth implementation status matrix
└── README.md                 # Primary project documentation
```

---

# 7. Python Environment

Python virtual environments isolate project dependencies from your system's global Python installation.

### Step-by-Step Python Setup (Windows)

```powershell
# 1. Navigate to the backend directory
cd C:\Projects\autonomous-se-platform\backend

# 2. Create a virtual environment named '.venv'
python -m venv .venv

# 3. Activate the virtual environment in PowerShell
.\.venv\Scripts\Activate.ps1

# (If PowerShell displays an ExecutionPolicy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# and re-run .\.venv\Scripts\Activate.ps1)

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install backend dependencies in editable mode with development tools
pip install -e .[dev]
```

---

# 8. Frontend Setup

The frontend is built using Next.js 16, React 19, TypeScript, and Tailwind CSS.

### Step-by-Step Frontend Setup

```powershell
# 1. Navigate to the frontend directory
cd C:\Projects\autonomous-se-platform\frontend

# 2. Install all Node.js package dependencies
npm install

# 3. Create frontend environment file from template
copy .env.example .env.local

# 4. Verify package installation succeeded without errors
```

---

# 9. Backend Setup

### Step-by-Step Backend Setup

```powershell
# 1. Navigate to the backend directory
cd C:\Projects\autonomous-se-platform\backend

# 2. Create backend environment file from template
copy .env.example .env

# 3. Apply database migrations using Alembic (Ensure PostgreSQL is running)
alembic upgrade head
```

---

# 10. Redis Setup

Redis acts as the message broker for Celery background tasks and caches repository summaries.

### Starting Redis via Docker
```powershell
docker run -d --name redis-server -p 6379:6379 redis:7-alpine
```

### Verifying Redis
```powershell
docker exec -it redis-server redis-cli ping
# Expected output: PONG
```

---

# 11. PostgreSQL Setup

PostgreSQL stores persistent data such as users, repositories, runs, and timeline events.

### Step 1: Starting PostgreSQL via Docker
```powershell
docker run -d --name postgres-db `
  -e POSTGRES_DB=autose_platform `
  -e POSTGRES_USER=autose_user `
  -e POSTGRES_PASSWORD=autose_password `
  -p 5432:5432 postgres:16-alpine
```

### Step 2: Connection String Format
The `DATABASE_URL` in `backend/.env` is formatted as:
`postgresql+asyncpg://autose_user:autose_password@localhost:5432/autose_platform`

---

# 12. Docker Setup

Docker Desktop allows you to launch the entire multi-container stack with a single command.

### Key Docker Commands
```powershell
# Start all containers in background
docker-compose up --build -d

# View real-time container logs
docker-compose logs -f

# Check running container statuses
docker-compose ps

# Stop all running containers
docker-compose down
```

---

# 13. Environment Variables

### Backend Environment Variables (`backend/.env`)

| Variable Name | Required | Default Value | Description |
| :--- | :---: | :--- | :--- |
| `ENV` | Yes | `development` | Runtime mode (`development` or `production`) |
| `DATABASE_URL` | Yes | `postgresql+asyncpg://...` | Connection URI for PostgreSQL database |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Connection URI for Redis server |
| `SECRET_KEY` | Yes | `dev-only-change-me` | 32-character secret key for JWT token signing |
| `WEBHOOK_SECRET` | Yes | `dev-webhook-secret` | Secret for GitHub HMAC SHA256 signature verification |
| `AI_PROVIDER` | Yes | `gemini` | Active primary LLM provider (`gemini`, `openai`, `groq`, `ollama`) |
| `GOOGLE_API_KEY` | Optional | `""` | API key for Google Gemini provider |
| `MODEL_NAME` | Optional | `gemini-1.5-flash` | Default Gemini chat model name |
| `OPENAI_API_KEYS` | Optional | `[]` | Comma-separated API keys for OpenAI |
| `GROQ_API_KEYS` | Optional | `[]` | Comma-separated API keys for Groq |

### Frontend Environment Variables (`frontend/.env.local`)

| Variable Name | Required | Default Value | Description |
| :--- | :---: | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000/api/v1` | Base URL of the backend REST API |

---

# 14. API Keys

### 1. Google Gemini API Key
- **Website**: [https://aistudio.google.com/](https://aistudio.google.com/)
- **Free Tier**: Available (Free tier with rate limits).
- **How to Create**: Sign in to Google AI Studio, click **Get API key**, click **Create API key in new project**, and copy the resulting string (`AIzaSy...`).
- **Where to Paste**: In `backend/.env` under `GOOGLE_API_KEY=AIzaSy...`.

### 2. OpenAI API Key
- **Website**: [https://platform.openai.com/](https://platform.openai.com/)
- **How to Create**: Go to API Keys tab, click **Create new secret key**, copy key (`sk-...`).
- **Where to Paste**: In `backend/.env` under `OPENAI_API_KEYS=sk-...`.

### 3. Groq API Key
- **Website**: [https://console.groq.com/](https://console.groq.com/)
- **Free Tier**: Available (High-speed inference free tier).
- **How to Create**: Sign in to Groq Console, click **API Keys**, click **Create API Key**, copy key (`gsk_...`).
- **Where to Paste**: In `backend/.env` under `GROQ_API_KEYS=gsk_...`.

### 4. JWT Secret Key
- **Purpose**: Cryptographic signature key for signing user authentication JWT tokens.
- **Generation**: Generate a random 32-character string in PowerShell:
  ```powershell
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- **Where to Paste**: In `backend/.env` under `SECRET_KEY=...`.

---

# 15. Running the Project

You can run the platform using **Docker Compose (Method A)** or **Individual Terminal Services (Method B)**.

---

# 16. Running with Docker

This is the simplest method for running the complete application.

```powershell
# 1. Move to the root directory
cd C:\Projects\autonomous-se-platform

# 2. Build and start all services
docker-compose up --build -d

# 3. Confirm all 6 containers are healthy
docker-compose ps
```

### Access Points
- **Frontend Dashboard**: Open `http://localhost` in your browser.
- **Backend API Health Check**: Open `http://localhost/api/v1/health`.
- **Prometheus Telemetry**: Open `http://localhost/api/v1/metrics/prometheus`.

---

# 17. Running without Docker

If you prefer to run services manually across separate terminal windows:

### Terminal 1: Infrastructure (PostgreSQL & Redis via Docker)
```powershell
docker run -d --name postgres-db -e POSTGRES_DB=autose_platform -e POSTGRES_USER=autose_user -e POSTGRES_PASSWORD=autose_password -p 5432:5432 postgres:16-alpine
docker run -d --name redis-server -p 6379:6379 redis:7-alpine
```

### Terminal 2: FastAPI Backend Server
```powershell
cd C:\Projects\autonomous-se-platform\backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

### Terminal 3: Celery Background Worker
```powershell
cd C:\Projects\autonomous-se-platform\backend
.\.venv\Scripts\Activate.ps1
celery -A app.workers.celery_app worker --loglevel=info -Q runs,dead_letter
```

### Terminal 4: Next.js Frontend Development Server
```powershell
cd C:\Projects\autonomous-se-platform\frontend
npm run dev
```

---

# 18. First Login

1. Open your web browser and navigate to `http://localhost` (or `http://localhost:3000`).
2. Click **"Sign In with GitHub"** at the top right of the dashboard.
3. In the modal, click **"Continue with GitHub OAuth"** (or click Demo Sign In).
4. Click **"Connect Repo"** in the navigation bar to register a new repository by providing its GitHub URL.
5. In the repository grid, click **"Launch Run"** to initiate an execution run and view real-time metrics in the **Cost & Health** panel.

---

# 19. Troubleshooting

### Issue 1: `python` command not recognized on Windows
- **Cause**: Python was installed without checking "Add python.exe to PATH".
- **Solution**: Re-run the Python installer, select **Modify**, and check **Add Python to environment variables**.

### Issue 2: PowerShell script execution disabled error
- **Cause**: Windows PowerShell default security policy blocks virtual environment activation.
- **Solution**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in PowerShell before running `Activate.ps1`.

### Issue 3: Port 5432 or 8000 already in use
- **Cause**: An existing PostgreSQL instance or local service is running on that port.
- **Solution**: Stop local PostgreSQL service via `services.msc` or identify and kill the process:
  ```powershell
  Get-Process -Id (Get-NetTCPConnection -LocalPort 5432).OwningProcess | Stop-Process -Force
  ```

---

# 20. Frequently Asked Questions

#### Q1: Can I run this project without any paid LLM API keys?
**Yes!** Set `AI_PROVIDER=ollama` in `backend/.env` and start a local Ollama instance (`http://localhost:11434`).

#### Q2: What happens if a primary LLM provider suffers an outage?
The platform automatically fails over through the resilient fallback chain (**Gemini → OpenAI → Groq → Ollama → Retry Queue**) using circuit breakers.

---

# 21. Common Commands

```powershell
# Activate Python Virtual Environment
cd backend; .\.venv\Scripts\Activate.ps1

# Run Pytest Backend Test Suite
pytest -v

# Run Golden Regression Suite
pytest tests/test_golden_regression.py -v

# Run MyPy Static Type Checker
mypy app tests

# Run Ruff Linter
ruff check app tests

# Start Docker Stack
docker-compose up --build -d

# Stop Docker Stack
docker-compose down
```

---

# 22. Verification Checklist

- [ ] `git --version`, `python --version`, `node -v`, and `docker --version` commands return valid versions.
- [ ] Backend virtual environment is created and dependencies installed via `pip install -e .[dev]`.
- [ ] Frontend dependencies installed via `npm install`.
- [ ] `backend/.env` file exists with valid `SECRET_KEY` and database URIs.
- [ ] PostgreSQL and Redis containers are healthy and reachable.
- [ ] All 49 Pytest backend tests pass cleanly (`pytest -v`).
- [ ] MyPy static type checks pass cleanly (`mypy app tests`).
- [ ] Frontend builds successfully (`npm run build`).
- [ ] Application web interface loads at `http://localhost`.
