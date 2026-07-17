import json
import os

import psycopg2
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="FastAPI Docker Demo",
    description="Minimal REST API demonstrating Docker Compose orchestration "
    "with Redis caching and PostgreSQL persistence.",
    version="1.0.0",
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not configured")
    try:
        return psycopg2.connect(database_url)
    except psycopg2.OperationalError as exc:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {exc}") from exc


@app.get("/")
def root():
    return {"message": "Hello from Docker Compose!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo(body: dict):
    """Echo the request body back, logging the request in PostgreSQL."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api_requests (endpoint, method, request_body, response_body, status_code)
                VALUES (%s, %s, %s, %s, %s)
                """,
                ("/echo", "POST", json.dumps(body), json.dumps(body), 200),
            )
        conn.commit()
    finally:
        conn.close()
    return body


@app.get("/requests")
def get_requests(limit: int = 10):
    """Return the most recent requests logged in PostgreSQL."""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, endpoint, method, request_body, status_code, created_at
                FROM api_requests
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cursor.fetchall()
    finally:
        conn.close()

    return [
        {
            "id": row[0],
            "endpoint": row[1],
            "method": row[2],
            "request_body": row[3],
            "status_code": row[4],
            "created_at": str(row[5]),
        }
        for row in rows
    ]


@app.post("/cache/{key}")
def set_cache(key: str, body: dict):
    """Store a value in Redis with a TTL."""
    try:
        redis_client.setex(key, CACHE_TTL_SECONDS, json.dumps(body))
    except redis.exceptions.ConnectionError as exc:
        raise HTTPException(status_code=503, detail=f"Redis unavailable: {exc}") from exc
    return {"message": f"Stored '{key}' for {CACHE_TTL_SECONDS} seconds"}


@app.get("/cache/{key}")
def get_cache(key: str):
    """Retrieve a cached value from Redis."""
    try:
        value = redis_client.get(key)
    except redis.exceptions.ConnectionError as exc:
        raise HTTPException(status_code=503, detail=f"Redis unavailable: {exc}") from exc
    if value is None:
        raise HTTPException(status_code=404, detail=f"Key '{key}' not found or expired")
    return {"key": key, "value": json.loads(value)}
