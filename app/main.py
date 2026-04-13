from fastapi import FastAPI
import redis
import psycopg2
import os
import json

app = FastAPI()

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


@app.get("/")
def root():
    return {"message": "Hello from Docker Compose!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/echo")
def echo(body: dict):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO api_requests (endpoint, method, request_body, response_body, status_code)
        VALUES (%s, %s, %s, %s, %s)
        """,
        ("/echo", "POST", json.dumps(body), json.dumps(body), 200)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return body


@app.get("/requests")
def get_requests():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, endpoint, method, request_body, status_code, created_at
        FROM api_requests
        ORDER BY created_at DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "endpoint": row[1],
            "method": row[2],
            "request_body": row[3],
            "status_code": row[4],
            "created_at": str(row[5])
        }
        for row in rows
    ]


@app.post("/cache/{key}")
def set_cache(key: str, body: dict):
    redis_client.setex(key, 60, str(body))
    return {"message": f"Stored '{key}' for 60 seconds"}


@app.get("/cache/{key}")
def get_cache(key: str):
    value = redis_client.get(key)
    if value is None:
        return {"message": f"Key '{key}' not found or expired"}
    return {"key": key, "value": value}