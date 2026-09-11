import psycopg2, time

conn = psycopg2.connect(dbname = "pgqueue")
cur = conn.cursor()

with open("claim.sql", "r") as file:
    claim_query = file.read()

def claim():
    cur.execute(claim_query)
    row = cur.fetchone()
    conn.commit()
    return row

def task_a(payload):
    print("working on task_a")

HANDLERS = {
    "a" : task_a
}

while True:
    job = claim()
    if job is None:
        time.sleep(3)
        continue
    payload = job[1]
    handler = HANDLERS.get(payload['task'])
    if handler is None:
        query = ("UPDATE jobs SET status = 'dead' WHERE id = %s;")
        data = (job[0],)
        cur.execute(query, data)
        conn.commit()
        continue
    try:
        handler(payload)
    except Exception:
        query = ("""UPDATE jobs
                  SET status = CASE
                  WHEN attempts >= max_attempts THEN 'dead'
                  ELSE 'queued'
                  END,
                  locked_by = NULL,
                  locked_until = NULL
                  WHERE id = %s;""")
        data = (job[0],)
        cur.execute(query, data)
        conn.commit()
    else:
        query = ("UPDATE jobs SET status = 'completed', locked_by = NULL, locked_until = NULL WHERE id = %s AND locked_by = %s;")
        data = (job[0], job[4])
        cur.execute(query, data)
        conn.commit()














