CREATE TABLE jobs(
    id bigserial PRIMARY KEY,
    payload jsonb NOT NULL,
    status text NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'dead')),
    created_at timestamptz NOT NULL DEFAULT now(),
    locked_by text,
    locked_until timestamptz,
    timeout_seconds int NOT NULL DEFAULT 30,
    attempts int NOT NULL DEFAULT 0,
    max_attempts int NOT NULL DEFAULT 3,
    run_at timestamptz NOT NULL DEFAULT now()
);

