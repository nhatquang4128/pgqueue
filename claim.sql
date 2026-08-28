UPDATE jobs
SET status = 'processing', locked_by = 'worker-1', locked_until = now() + (timeout_seconds || ' seconds')::interval, attempts = attempts + 1
WHERE id = (SELECT id from jobs
            WHERE status = 'queued' AND run_at <= now()
            ORDER BY created_at
            LIMIT 1
            FOR UPDATE SKIP LOCKED)
