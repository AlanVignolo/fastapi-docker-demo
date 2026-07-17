# FastAPI Docker Demo

[![CI](https://github.com/AlanVignolo/fastapi-docker-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/AlanVignolo/fastapi-docker-demo/actions/workflows/ci.yml)

A minimal REST API built with FastAPI and Docker, demonstrating containerization best practices, multi-service orchestration with Docker Compose, Redis caching, and PostgreSQL persistence.

## Tech Stack

- **FastAPI** — REST API framework
- **Docker & Docker Compose** — containerization and orchestration
- **Redis** — in-memory caching with TTL
- **PostgreSQL** — request logging / persistence
- **Pytest + GitHub Actions** — tests and CI
- **Python 3.11**

## Architecture

```
                ┌─────────────┐
   :8000  ───►  │  api        │
                │  (FastAPI)  │
                └──────┬──────┘
              ┌────────┴────────┐
              ▼                 ▼
      ┌──────────────┐  ┌──────────────┐
      │  redis       │  │  db          │
      │  (cache/TTL) │  │  (Postgres)  │
      └──────────────┘  └──────────────┘
```

Three services on a shared Docker network: the API caches values in Redis and logs requests to PostgreSQL. The database schema is created automatically on first start via `db/init.sql`.

## Project Structure

```
fastapi-docker-demo/
├── app/
│   └── main.py             # API endpoints
├── db/
│   └── init.sql            # Schema, applied on first container start
├── tests/
│   └── test_api.py         # API tests (DB/Redis mocked)
├── .github/workflows/
│   └── ci.yml              # Lint + tests + Docker build
├── Dockerfile              # Multi-stage image definition
├── docker-compose.yml      # Multi-service orchestration
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Dev dependencies (pytest, ruff)
└── .env.example            # Environment variables template
```

## Getting Started

### Prerequisites

- Docker Desktop installed and running
- Git

### Run with Docker Compose

1. Clone the repository

   ```bash
   git clone https://github.com/AlanVignolo/fastapi-docker-demo.git
   cd fastapi-docker-demo
   ```

2. Set up environment variables

   ```bash
   cp .env.example .env
   ```

3. Start all services

   ```bash
   docker-compose up -d
   ```

4. Open the interactive API docs

   http://localhost:8000/docs

### Run locally (without Docker)

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Note: without Docker you need Redis and PostgreSQL reachable via `REDIS_HOST` and `DATABASE_URL`.

### Run tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

Tests mock Redis and PostgreSQL, so no services are required.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/echo` | Echoes the request body and logs it to PostgreSQL |
| GET | `/requests` | Last N logged requests from PostgreSQL (`?limit=10`) |
| POST | `/cache/{key}` | Stores a JSON value in Redis (configurable TTL) |
| GET | `/cache/{key}` | Retrieves a cached value (404 if missing/expired) |

## Key Concepts Demonstrated

- **Multi-stage Docker builds** — optimized image layers for faster builds
- **Docker Compose orchestration** — API, Redis and PostgreSQL as isolated services in the same network, with `depends_on` + health-check conditions
- **Database initialization** — schema applied automatically via `/docker-entrypoint-initdb.d`
- **Environment variables** — all configuration via `.env`, no hardcoded credentials
- **Health checks & restart policies** — Docker monitors and recovers services
- **Redis caching** — in-memory storage with automatic key expiration
- **Error handling** — proper HTTP status codes (404, 503) when dependencies are down
- **CI pipeline** — lint (ruff), tests (pytest) and Docker build on every push

## Docker Commands Reference

```bash
docker-compose up -d          # Start all services in background
docker-compose down           # Stop and remove containers
docker-compose down -v        # Also remove volumes (resets the database)
docker-compose logs -f        # Follow logs from all services
docker-compose ps             # Check service status and health
docker exec -it <container> bash  # Enter a running container
docker history <image>        # Inspect image layers
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENV` | Environment name | `development` |
| `APP_NAME` | Application name | `fastapi-docker-demo` |
| `SECRET_KEY` | Secret key for the app | — |
| `POSTGRES_USER` | PostgreSQL user | `demo` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `demo_password` |
| `POSTGRES_DB` | PostgreSQL database name | `fastapi_demo` |
| `DATABASE_URL` | Full PostgreSQL connection string | — |
| `REDIS_HOST` | Redis hostname | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `CACHE_TTL_SECONDS` | Cache expiration time | `60` |
