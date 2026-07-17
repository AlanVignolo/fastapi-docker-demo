from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Docker Compose!"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo_returns_body_and_logs_to_db(monkeypatch):
    fake_conn = MagicMock()
    monkeypatch.setattr(main, "get_db_connection", lambda: fake_conn)

    response = client.post("/echo", json={"hello": "world"})

    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
    fake_conn.commit.assert_called_once()
    fake_conn.close.assert_called_once()


class FakeRedis:
    """Minimal in-memory stand-in for the Redis client."""

    def __init__(self):
        self.store = {}

    def setex(self, key, ttl, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key)


def test_cache_roundtrip(monkeypatch):
    monkeypatch.setattr(main, "redis_client", FakeRedis())

    set_response = client.post("/cache/mykey", json={"value": 42})
    assert set_response.status_code == 200

    get_response = client.get("/cache/mykey")
    assert get_response.status_code == 200
    assert get_response.json() == {"key": "mykey", "value": {"value": 42}}


def test_cache_missing_key_returns_404(monkeypatch):
    monkeypatch.setattr(main, "redis_client", FakeRedis())

    response = client.get("/cache/does-not-exist")
    assert response.status_code == 404
