import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME_SQLITE")

sql_statements = [
    """CREATE TABLE IF NOT EXISTS phase (
            id INTEGER PRIMARY KEY,
            name text NOT NULL UNIQUE
        );""",
    """CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY, 
            name text NOT NULL UNIQUE,
            phase_id INT NOT NULL,
            FOREIGN KEY (phase_id) REFERENCES phase (id),
            UNIQUE (id, phase_id)
        );""",
    """CREATE TABLE IF NOT EXISTS application (
            id INTEGER PRIMARY KEY, 
            company_name text NOT NULL,
            job_title text NOT NULL, 
            URL text, 
            status_id INT NOT NULL,
            date_added DATE NOT NULL,
            date_appointment DATE,
            FOREIGN KEY (status_id) REFERENCES status (id)
        );""",
    # enforces that logged status and phase both exist as primary keys status table
    """CREATE TABLE IF NOT EXISTS application_history_log (
            id INTEGER PRIMARY KEY,
            application_id INT NOT NULL,
            phase_id INT NOT NULL,
            status_id INT NOT NULL,
            occurred_at DATE NOT NULL,
            FOREIGN KEY (application_id) REFERENCES application (id) ON DELETE CASCADE,
            FOREIGN KEY (phase_id, status_id) REFERENCES status (phase_id, id)
        );""",
]

try:
    with sqlite3.connect("application_tracker.db") as conn:
        cursor = conn.cursor()

        for statement in sql_statements:
            cursor.execute(statement)

        conn.commit()

        print("Tables created successfully.")
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
