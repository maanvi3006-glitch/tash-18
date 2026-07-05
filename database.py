"""
database.py
------------
Centralized database connection utility for the PlaceMux platform.

All modules and dashboard pages should import `get_connection()` from
this file rather than opening their own sqlite3 connections. This keeps
connection settings (row factory, foreign keys, path resolution)
consistent across the whole project.
"""

import os
import sqlite3

# Absolute path to the SQLite database file, regardless of the caller's
# current working directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "placemux.db")


def get_connection():
    """
    Create and return a new SQLite connection to the PlaceMux database.

    The connection is configured with:
    - row_factory = sqlite3.Row, so query results can be accessed both
      by column name and by index.
    - foreign_keys = ON, to enforce referential integrity.

    Returns:
        sqlite3.Connection: An open database connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def run_query(query, params=None):
    """
    Execute a SELECT query and return the results as a list of sqlite3.Row.

    Args:
        query (str): The SQL query to execute.
        params (tuple | dict | None): Optional bound parameters.

    Returns:
        list[sqlite3.Row]: Query result rows.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        return cursor.fetchall()
    finally:
        conn.close()


def execute_write(query, params=None):
    """
    Execute an INSERT / UPDATE / DELETE statement and commit the change.

    Args:
        query (str): The SQL statement to execute.
        params (tuple | dict | None): Optional bound parameters.

    Returns:
        int: The number of rows affected.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def database_exists():
    """Check whether the SQLite database file has already been created."""
    return os.path.exists(DB_PATH)
