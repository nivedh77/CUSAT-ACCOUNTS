
import sqlite3
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

# Find the project folder and database file.
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "events.db"

def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.HTML")

@app.route("/style.css")
def stylesheet():
    return send_from_directory(BASE_DIR, "style.css")

@app.route("/api/main-events", methods=["GET"])
def get_main_events():
    connection = get_db_connection()

    try:
        rows = connection.execute(
            """
            SELECT id, name, description, event_date
            FROM main_events
            ORDER BY id DESC
            """
        ).fetchall()

        events = [dict(row) for row in rows]
        return jsonify(events)

    finally:
        connection.close()

@app.route("/api/main-events", methods=["POST"])
def create_main_event():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    description = data.get("description", "").strip()
    event_date = data.get("event_date", "").strip()

    if not name or not event_date:
        return jsonify({
            "error": "Event name and date are required."
        }), 400

    connection = get_db_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO main_events (name, description, event_date)
            VALUES (?, ?, ?)
            """,
            (name, description, event_date)
        )

        connection.commit()

        return jsonify({
            "message": "Main event created successfully.",
            "id": cursor.lastrowid,
            "name": name,
            "description": description,
            "event_date": event_date
        }), 201

    finally:
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)