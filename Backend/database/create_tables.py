import sqlite3

sql_statements = [ 
    """CREATE TABLE IF NOT EXISTS phase (
            id INTEGER PRIMARY KEY,
            name text NOT NULL UNIQUE
        );""",

    """CREATE TABLE IF NOT EXISTS status (
            id INTEGER PRIMARY KEY, 
            name text NOT NULL UNIQUE,
            phase_id INT NOT NULL,
            FOREIGN KEY (phase_id) REFERENCES phase (id)
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