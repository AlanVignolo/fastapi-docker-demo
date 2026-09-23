# FastAPI Docker Demo

This is a practice exercise, not a product: I built it to learn how to containerize a Python API with Docker Compose, wiring in Redis and PostgreSQL as separate services.

[![CI](https://github.com/AlanVignolo/fastapi-docker-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/AlanVignolo/fastapi-docker-demo/actions/workflows/ci.yml)

## Stack

FastAPI, Redis (cache with TTL), PostgreSQL (request log), Docker Compose. Three services on one network — the API talks to both, `db/init.sql` creates the schema on first start.

## Run it

```bash
cp .env.example .env
docker-compose up -d
```

Docs at http://localhost:8000/docs.

Locally, without Docker:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

You'll need Redis and PostgreSQL reachable via `REDIS_HOST` and `DATABASE_URL` in that case.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root |
| GET | `/health` | Health check |
| POST | `/echo` | Echoes the body, logs it to PostgreSQL |
| GET | `/requests` | Last N logged requests (`?limit=10`) |
| POST | `/cache/{key}` | Stores a value in Redis with TTL |
| GET | `/cache/{key}` | Reads it back, 404 if missing or expired |

## What's missing

No authentication — every endpoint is open. Never deployed or tested outside `docker-compose` on my machine, so I don't know how it behaves under real load or a real network. Tests mock Redis and PostgreSQL entirely, so they don't catch connection issues with the real services.
