"""
modules/utils.py
------------------
Shared utility functions used across recruiter, review queue, admin,
and analytics modules: query loading, CSV export helpers, and common
formatting helpers.
"""

import os
import re

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUERIES_PATH = os.path.join(BASE_DIR, "sql", "queries.sql")


def load_named_queries():
    """
    Parse sql/queries.sql into a dictionary of {name: query_string}.

    Queries in the .sql file are annotated with a comment of the form:
        -- name: query_identifier
    immediately preceding the SQL statement.

    Returns:
        dict[str, str]: Mapping of query name to SQL text.
    """
    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Split the file on the "-- name: xxx" markers.
    pattern = re.compile(r"--\s*name:\s*(\w+)\s*\n(.*?)(?=(--\s*name:|\Z))", re.DOTALL)
    queries = {}
    for match in pattern.finditer(content):
        name = match.group(1).strip()
        sql_text = match.group(2).strip().rstrip(";")
        queries[name] = sql_text
    return queries


def get_query(name):
    """
    Fetch a single named query from sql/queries.sql.

    Args:
        name (str): The query identifier (e.g. 'top_recruiters_by_placement_rate').

    Returns:
        str: The raw SQL text (without trailing semicolon).
    """
    queries = load_named_queries()
    if name not in queries:
        raise KeyError(f"Query '{name}' not found in sql/queries.sql")
    return queries[name]


def rows_to_dataframe(rows):
    """
    Convert a list of sqlite3.Row objects into a pandas DataFrame.

    Args:
        rows (list[sqlite3.Row]): Rows returned from database.run_query().

    Returns:
        pd.DataFrame: A DataFrame with columns matching the row keys.
    """
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame([dict(row) for row in rows])


def dataframe_to_csv_bytes(df):
    """
    Convert a DataFrame to UTF-8 encoded CSV bytes, suitable for
    Streamlit's st.download_button.

    Args:
        df (pd.DataFrame): The DataFrame to export.

    Returns:
        bytes: CSV-encoded content.
    """
    return df.to_csv(index=False).encode("utf-8")


def apply_text_filter(df, column, value):
    """
    Apply a case-insensitive substring filter to a DataFrame column,
    only if a non-empty value is supplied.

    Args:
        df (pd.DataFrame): Source DataFrame.
        column (str): Column name to filter on.
        value (str): Substring to search for.

    Returns:
        pd.DataFrame: Filtered DataFrame (or original if value is empty).
    """
    if value and column in df.columns:
        return df[df[column].astype(str).str.contains(value, case=False, na=False)]
    return df


def apply_exact_filter(df, column, value):
    """
    Apply an exact-match filter to a DataFrame column, only if the
    value is not the sentinel "All".

    Args:
        df (pd.DataFrame): Source DataFrame.
        column (str): Column name to filter on.
        value (str): Value to match exactly.

    Returns:
        pd.DataFrame: Filtered DataFrame (or original if value is "All").
    """
    if value and value != "All" and column in df.columns:
        return df[df[column] == value]
    return df


def apply_date_range_filter(df, column, start_date, end_date):
    """
    Filter a DataFrame to rows where `column` (a date-like string column)
    falls within [start_date, end_date].

    Args:
        df (pd.DataFrame): Source DataFrame.
        column (str): Column name holding date strings (YYYY-MM-DD).
        start_date (datetime.date): Range start (inclusive).
        end_date (datetime.date): Range end (inclusive).

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if column not in df.columns:
        return df
    dates = pd.to_datetime(df[column], errors="coerce")
    mask = (dates.dt.date >= start_date) & (dates.dt.date <= end_date)
    return df[mask]


def format_percentage(value):
    """Format a numeric value as a percentage string with 2 decimal places."""
    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return "N/A"
