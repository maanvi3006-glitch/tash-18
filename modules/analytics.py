"""
modules/analytics.py
----------------------
Business logic that aggregates data for the Analytics Dashboard's
Plotly visualizations.
"""

from database import run_query
from modules.utils import get_query, rows_to_dataframe


def get_recruiter_performance_leaderboard():
    """Full recruiter performance table used for the leaderboard chart."""
    rows = run_query(get_query("recruiter_performance_full"))
    return rows_to_dataframe(rows)


def get_placement_rate_by_recruiter(limit=15):
    """Top N recruiters by placement rate, for bar chart display."""
    df = get_recruiter_performance_leaderboard()
    if df.empty:
        return df
    return df.sort_values("placement_rate", ascending=False).head(limit)


def get_jobs_posted_by_company():
    """Job counts grouped by company."""
    rows = run_query(get_query("jobs_by_company"))
    return rows_to_dataframe(rows)


def get_applications_by_status():
    """Application counts grouped by status."""
    rows = run_query(get_query("applications_by_status"))
    return rows_to_dataframe(rows)


def get_review_queue_status_distribution():
    """Review queue item counts grouped by review status."""
    rows = run_query(get_query("review_queue_status_distribution"))
    return rows_to_dataframe(rows)


def get_company_verification_status():
    """Company counts grouped by verification status."""
    rows = run_query(get_query("company_verification_distribution"))
    return rows_to_dataframe(rows)


def get_monthly_recruiter_registrations():
    """Recruiter registration counts grouped by month."""
    rows = run_query(get_query("monthly_recruiter_registrations"))
    return rows_to_dataframe(rows)


def get_hiring_funnel():
    """Aggregate hiring funnel stage counts (applied -> hired)."""
    rows = run_query(get_query("hiring_funnel"))
    return dict(rows[0]) if rows else {}


def get_placement_statistics():
    """Overall placement statistics (totals and averages)."""
    rows = run_query(get_query("placement_statistics"))
    return dict(rows[0]) if rows else {}
