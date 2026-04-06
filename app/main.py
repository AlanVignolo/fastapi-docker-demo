from fastapi import FastAPI
import redis
import os

app = FastAPI()

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

@app.get("/")
def root():
    return {"message": "Hello from Docker Compose!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(body: dict):
    return body

@app.post("/cache/{key}")
def set_cache(key:str, body: dict):
    redis_client.setex(key, 60, str(body))
    return {"message": f"Stored '{key}' for 60 seconds"}

@app.get("/cache/{key}")
def get_cache(key:str):
    value = redis_client.get(key)
    if value is None:
        return {"message": f"Key 'key' not found or expired"}
    return {"key": key, "value": value}
