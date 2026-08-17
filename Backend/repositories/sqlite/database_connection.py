import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path
from repositories.sqlite.sqlite_repository_factory import SqliteRepositoryFactory

BASE_DIR = Path(__file__).parent

load_dotenv()

DATABASE_NAME = BASE_DIR / "database" / os.getenv("DATABASE_NAME_SQLITE")


def get_sqlite_repository_factory():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    # enable foreign keys constraints for current connection (does not persist - runs on each new connection)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield SqliteRepositoryFactory(conn)
    finally:
        conn.close()
