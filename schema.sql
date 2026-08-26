CREATE TABLE jobs(
    id bigserial PRIMARY KEY,
    payload jsonb NOT NULL,
    status text NOT NULL DEFAULT 'queued' CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'dead')),
    created_at timestamptz NOT NULL DEFAULT now()
);

