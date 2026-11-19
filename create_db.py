import sqlite3
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parent
SCHEMA_PATH=BASE_DIR/"database"/"events.sql"
DB_PATH=BASE_DIR/"database"/"events.db"
if not SCHEMA_PATH.exists():
    raise FileNotFoundError(f"SCHEME NOT FOUND:{SCHEMA_PATH}")
schema=SCHEMA_PATH.read_text(encoding="utf-8")
with sqlite3.connect(DB_PATH)as connection:
    connection.execute("PRAGMA foreign_keys=ON")
try:
    connection.executescript(schema)
except sqlite3.Error as error:
    print("SQLITE error:",error)
    raise
    
    print(f"DATABASE CREATED SUCCESSFULLY:{DB_PATH}")




with sqlite3.connect(DB_PATH)as connection:
    result=connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )    
    print("TABLES FOUND:",result.fetchall())
with sqlite3.connect(DB_PATH) as connection:

    cursor = connection.execute(
        "PRAGMA table_info(events)"
    )

    columns = cursor.fetchall()

    print("EVENTS TABLE STRUCTURE:")

for column in columns:
    print("Column name:", column[1])   
with sqlite3.connect(DB_PATH) as connection:

    tables = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    print("DATABASE TABLES:")

    for table in tables:
        print(table[0])
    
    connection.commit()

print("Migration successful: event_name column added.")
with sqlite3.connect(DB_PATH) as connection:

    records = connection.execute(
        "SELECT * FROM financial_records"
    ).fetchall()

    print("\nALL FINANCIAL RECORDS:")

    for record in records:
        print(record)