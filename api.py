from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

conn = psycopg2.connect(dbname="pgqueue")
cur = conn.cursor()

app = FastAPI()
class JobRequest(BaseModel):
    model_config = {"extra": "allow"}
    task: str

@app.get("/health")
def health():
    return {"status" : "OK"}

@app.post("/jobs")
def post():
    pass




