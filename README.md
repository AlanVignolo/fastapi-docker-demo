# FastAPI Docker Demo

A minimal REST API built with FastAPI and Docker, demonstrating containerization best practices, multi-service orchestration with Docker Compose, and Redis integration for caching.

## Tech Stack

- **FastAPI** — REST API framework
- **Docker & Docker Compose** — containerization and orchestration
- **Redis** — in-memory caching
- **Python 3.11**

## Project Structure

fastapi-docker-demo/
├── app/
│   └── main.py         # API endpoints
├── Dockerfile          # Image definition
├── docker-compose.yml  # Multi-service orchestration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md


## Getting Started

### Prerequisites

- Docker Desktop installed and running
- Git

### Run with Docker Compose

1. Clone the repository

   git clone https://github.com/AlanVignolo/fastapi-docker-demo.git
   cd fastapi-docker-demo

2. Set up environment variables

   cp .env.example .env

3. Start all services

   docker-compose up -d

4. Open the interactive API docs

   http://localhost:8000/docs

### Run locally (without Docker)

1. Create and activate a virtual environment

   python -m venv .venv
   source .venv/Scripts/activate  # Windows Git Bash

2. Install dependencies

   pip install -r requirements.txt

3. Start the server

   uvicorn app.main:app --reload

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/echo` | Echoes the request body |
| POST | `/cache/{key}` | Stores a value in Redis (60s TTL) |
| GET | `/cache/{key}` | Retrieves a cached value |

## Key Concepts Demonstrated

- **Multi-stage Docker builds** — optimized image layers for faster builds
- **Docker Compose orchestration** — API and Redis running as isolated services in the same network
- **Environment variables** — configuration via `.env` file, never hardcoded
- **Health checks** — Docker monitors service health automatically
- **Restart policies** — automatic container recovery on failure
- **Redis caching** — in-memory storage with automatic key expiration

## Docker Commands Reference
```bash
docker-compose up -d          # Start all services in background
docker-compose down           # Stop and remove containers
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