
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
@app.route("/api/sub-events", methods=["GET"])
def get_sub_events():

    main_event_id = request.args.get("main_event_id")

    if not main_event_id:
        return jsonify({"error": "Main event ID is required."}), 400

    connection = get_db_connection()

    try:
        rows = connection.execute(
            """
            SELECT id, main_event_id, event_name,
                   department, event_date, status
            FROM events
            WHERE main_event_id = ?
            ORDER BY id DESC
            """,
            (main_event_id,)
        ).fetchall()

        return jsonify([dict(row) for row in rows])

    finally:
        connection.close()


@app.route("/api/sub-events", methods=["POST"])
def create_sub_event():

    data = request.get_json(silent=True) or {}

    main_event_id = data.get("main_event_id")
    event_name = data.get("event_name", "").strip()
    department = data.get("department", "CUCEK").strip()
    event_date = data.get("event_date", "").strip()

    if not main_event_id or not event_name or not event_date:
        return jsonify({
            "error": "Main event, sub-event name and date are required."
        }), 400

    connection = get_db_connection()

    try:
        parent = connection.execute(
            "SELECT id FROM main_events WHERE id = ?",
            (main_event_id,)
        ).fetchone()

        if parent is None:
            return jsonify({"error": "Main event not found."}), 404

        cursor = connection.execute(
            """
            INSERT INTO events
            (main_event_id, event_name, department, event_date)
            VALUES (?, ?, ?, ?)
            """,
            (main_event_id, event_name, department, event_date)
        )

        connection.commit()

        return jsonify({
            "message": "Sub-event created successfully.",
            "id": cursor.lastrowid
        }), 201

    finally:
        connection.close()
@app.route("/api/financial-records", methods=["GET"])
def get_financial_records():

    event_id = request.args.get("event_id")

    if not event_id:
        return jsonify({"error": "Event ID is required."}), 400

    connection = get_db_connection()

    try:
        records = connection.execute(
            """
            SELECT *
            FROM financial_records
            WHERE event_id = ?
            ORDER BY transaction_date DESC
            """,
            (event_id,)
        ).fetchall()

        return jsonify([dict(record) for record in records])

    finally:
        connection.close()


@app.route("/api/financial-records", methods=["POST"])
def create_financial_record():

    data = request.get_json(silent=True) or {}

    event_id = data.get("event_id")
    record_type = data.get("record_type")
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    transaction_date = data.get("transaction_date", "").strip()

    try:
        amount = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid amount."}), 400

    if not event_id or not category or not transaction_date:
        return jsonify({"error": "Please fill all required fields."}), 400

    if record_type not in ("Income", "Expense"):
        return jsonify({"error": "Invalid transaction type."}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero."}), 400

    connection = get_db_connection()

    try:
        event = connection.execute(
            "SELECT id FROM events WHERE id = ?",
            (event_id,)
        ).fetchone()

        if event is None:
            return jsonify({"error": "Sub-event not found."}), 404

        cursor = connection.execute(
            """
            INSERT INTO financial_records
            (event_id, record_type, category, description,
             amount, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                record_type,
                category,
                description,
                amount,
                transaction_date
            )
        )

        connection.commit()

        return jsonify({
            "message": "Financial record saved successfully.",
            "id": cursor.lastrowid
        }), 201

    finally:
        connection.close()    

@app.route("/api/financial-summary", methods=["GET"])
def financial_summary():

    event_id = request.args.get("event_id")

    if not event_id:
        return jsonify({"error": "Event ID required"}), 400

    connection = get_db_connection()

    try:
        summary = connection.execute(
            """
            SELECT
                COALESCE(SUM(CASE
                    WHEN record_type = 'Income'
                    THEN amount ELSE 0 END), 0) AS total_income,

                COALESCE(SUM(CASE
                    WHEN record_type = 'Expense'
                    THEN amount ELSE 0 END), 0) AS total_expenses

            FROM financial_records
            WHERE event_id = ?
            """,
            (event_id,)
        ).fetchone()

        income = summary["total_income"]
        expenses = summary["total_expenses"]

        return jsonify({
            "total_income": income,
            "total_expenses": expenses,
            "balance": income - expenses
        })

    finally:
        connection.close()



if __name__ == "__main__":
    app.run(debug=True)           

