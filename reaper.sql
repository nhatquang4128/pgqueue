UPDATE jobs
SET status = CASE
    WHEN attempts >= max_attempts THEN 'dead'
    ELSE 'queued'
END,
locked_by = NULL,
locked_until = NULL
WHERE status = 'processing' AND locked_until < now();
