import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path
from repositories.sqlite.sqlite_repository_factory import SqliteRepositoryFactory

BASE_DIR = Path(__file__).parent.parent

load_dotenv()

DATABASE_NAME = BASE_DIR / os.getenv("DATABASE_NAME_SQLITE")


def get_sqlite_repository_factory():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield SqliteRepositoryFactory(conn)
    finally:
        conn.close()
