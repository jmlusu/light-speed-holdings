import sqlite3

conn = sqlite3.connect("audit/audit.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)
for table in tables:
    cursor.execute(f"PRAGMA table_info({table[0]})")
    cols = cursor.fetchall()
    print(f"{table[0]} columns:", [c[1] for c in cols])
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()
    print(f"  Count: {count[0]}")
conn.close()
