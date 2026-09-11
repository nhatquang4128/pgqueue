import psycopg2, time

conn = psycopg2.connect(dbname = "pgqueue")
cur = conn.cursor()

with open ("reaper.sql", "r") as file:
    reaper_query = file.read()

while True:
    cur.execute(reaper_query)
    count = cur.rowcount
    conn.commit()
    if count != 0:
        print(f"Reclaimed {count} rows")
    time.sleep(10)



