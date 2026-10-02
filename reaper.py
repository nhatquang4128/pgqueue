import psycopg2, time

conn = psycopg2.connect(dbname = "pgqueue")
cur = conn.cursor()

with open ("reaper.sql", "r") as file:
    reaper_query = file.read()

while True:
    try:
        cur.execute(reaper_query)
    except Exception as e:
        conn.rollback()
        print(f"Query failed: {e}")
    else:
        count = cur.rowcount
        conn.commit()
        if count != 0:
            print(f"Reclaimed {count} rows")
    time.sleep(10)



