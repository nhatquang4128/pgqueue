import psycopg2, time

conn = psycopg2.connect(dbname = "pgqueue")
with open("claim.sql", "r") as file:
    claim_query = file.read()

def claim():
    cur = conn.cursor()
    cur.execute(claim_query)
    row = cur.fetchone()
    conn.commit()
    return row

while True:
    job = claim()
    if job is None:
        time.sleep(3)
        continue
    print(job)

