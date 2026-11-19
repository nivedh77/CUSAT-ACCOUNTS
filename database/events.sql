
PRAGMA foreign_keys = ON;

-- Main university events
CREATE TABLE IF NOT EXISTS main_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    event_date TEXT
);

-- Individual events and sub-events
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_event_id INTEGER,
    event_name TEXT NOT NULL,
    department TEXT NOT NULL DEFAULT 'CUCEK',
    event_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',

    FOREIGN KEY (main_event_id)
        REFERENCES main_events(id)
);

-- Financial transactions
CREATE TABLE IF NOT EXISTS financial_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    record_type TEXT NOT NULL
        CHECK (record_type IN ('Income', 'Expense')),
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL CHECK (amount > 0),
    transaction_date TEXT NOT NULL,
    receipt_filename TEXT,

    FOREIGN KEY (event_id)
        REFERENCES events(id)
);
    