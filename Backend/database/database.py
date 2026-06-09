import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent

load_dotenv()

DATABASE_NAME = BASE_DIR / os.getenv('DATABASE_NAME')

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
