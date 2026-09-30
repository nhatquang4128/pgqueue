from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import json
from datetime import datetime

conn = psycopg2.connect(dbname="pgqueue")
cur = conn.cursor()

app = FastAPI()
class JobRequest(BaseModel):
    model_config = {"extra": "allow"}
    task: str

class JobConfig(BaseModel):
    timeout_seconds: int | None = None
    max_attempts: int | None = None
    run_at: datetime | None = None

@app.get("/health")
def health():
    query = "SELECT 1;"
    try:
        cur.execute(query)
        return {"status": "OK"}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=503, detail="database unavailable")


@app.post("/jobs")
def post(job: JobRequest, config: JobConfig):
    payload = job.model_dump()
    row = json.dumps(payload)
    query = """INSERT INTO jobs (payload, timeout_seconds, max_attempts, run_at)
               VALUES (%s, COALESCE(%s, 30), COALESCE(%s, 3), COALESCE(%s, now()))
               RETURNING id;"""
    data = (row, config.timeout_seconds, config.max_attempts, config.run_at)
    try:
        cur.execute(query, data)
    except Exception:
        conn.rollback
        raise HTTPException(status_code=503, detail="database unavailable")
    job_id = cur.fetchone()[0]
    conn.commit()
    return {"id" : job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    query = """SELECT id, status, attempts, max_attempts, created_at, run_at FROM jobs WHERE id = %s;"""
    data = (job_id,)
    try:
        cur.execute(query, data)
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=503, detail="database unavailable")
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    else:
        return {"id": row[0], "status": row[1], "attempts": row[2], "max_attempts": row[3], "created_at": row[4], "run_at":row[5]}


