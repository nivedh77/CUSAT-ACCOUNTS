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