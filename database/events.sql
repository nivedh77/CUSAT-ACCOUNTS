
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS main_events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    event_date TEXT
);

CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    main_event_id INTEGER
    event_name TEXT NOT NULL,
    department TEXT  NOT NULL DEFAULT CUCEK,
    event_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (main_event_id)
    REFERENCES  main_events(id)
    );

    