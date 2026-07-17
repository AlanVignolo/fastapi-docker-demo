-- Runs automatically on first container start (mounted in /docker-entrypoint-initdb.d/)
CREATE TABLE IF NOT EXISTS api_requests (
    id SERIAL PRIMARY KEY,
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL,
    request_body JSONB,
    response_body JSONB,
    status_code INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_api_requests_created_at ON api_requests (created_at DESC);
