from fastapi import FastAPI
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
    return {"status" : "OK"}


@app.post("/jobs")
def post(job: JobRequest, config: JobConfig):
    payload = job.model_dump()
    row = json.dumps(payload)
    query = """INSERT INTO jobs (payload, timeout_seconds, max_attempts, run_at)
               VALUES (%s, COALESCE(%s, 30), COALESCE(%s, 3), COALESCE(%s, now()))
               RETURNING id;"""
    data = (row, config.timeout_seconds, config.max_attempts, config.run_at)
    cur.execute(query, data)
    job_id = cur.fetchone()[0]
    conn.commit()
    return {"id" : job_id}











