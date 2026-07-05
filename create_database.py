"""
create_database.py
--------------------
Initializes the PlaceMux SQLite database by executing sql/schema.sql.

Run this once (or whenever you want a clean slate) before generating
fake data:

    python create_database.py
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "placemux.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")


def create_database():
    """Create (or recreate) the placemux.db SQLite database using schema.sql."""
    # Ensure the data/ directory exists.
    os.makedirs(DATA_DIR, exist_ok=True)

    # Remove any existing database file for a clean initialization.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[create_database] Removed existing database at {DB_PATH}")

    # Read the schema definition.
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    # Execute the schema script against a fresh database file.
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print(f"[create_database] Database created successfully at {DB_PATH}")
    finally:
        conn.close()

    # Verify tables were created.
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"[create_database] Tables created: {', '.join(tables)}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
