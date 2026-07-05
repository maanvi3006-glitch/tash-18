"""
modules/recruiter.py
----------------------
Business logic for recruiter analytics and top-recruiter views.

Functions here query the database and return pandas DataFrames that
are consumed directly by the Streamlit dashboard pages.
"""

from database import run_query
from modules.utils import get_query, rows_to_dataframe


def get_all_recruiters():
    """
    Fetch all recruiters joined with their performance data (if any).

    Returns:
        pd.DataFrame: One row per recruiter with performance metrics.
    """
    query = """
        SELECT
            r.recruiter_id, r.name, r.company, r.email, r.industry,
            r.city, r.experience_years, r.status, r.joined_date,
            COALESCE(p.jobs_posted, 0) AS jobs_posted,
            COALESCE(p.applications_received, 0) AS applications_received,
            COALESCE(p.interviews, 0) AS interviews,
            COALESCE(p.offers_made, 0) AS offers_made,
            COALESCE(p.hires, 0) AS hires,
            COALESCE(p.placement_rate, 0.0) AS placement_rate
        FROM Recruiters r
        LEFT JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id
    """
    rows = run_query(query)
    return rows_to_dataframe(rows)


def get_top_recruiters_by_placement_rate():
    """Top 10 recruiters ranked by placement rate."""
    rows = run_query(get_query("top_recruiters_by_placement_rate"))
    return rows_to_dataframe(rows)


def get_top_recruiters_by_jobs_posted():
    """Top 10 recruiters ranked by number of jobs posted."""
    rows = run_query(get_query("top_recruiters_by_jobs_posted"))
    return rows_to_dataframe(rows)


def get_top_recruiters_by_offers():
    """Top 10 recruiters ranked by number of offers made."""
    rows = run_query(get_query("top_recruiters_by_offers"))
    return rows_to_dataframe(rows)


def get_top_recruiters_by_conversion():
    """Top 10 recruiters ranked by candidate conversion rate (hires/applications)."""
    rows = run_query(get_query("top_recruiters_by_conversion"))
    return rows_to_dataframe(rows)


def get_most_active_recruiters():
    """Top 10 most active recruiters ranked by applications received."""
    rows = run_query(get_query("most_active_recruiters"))
    return rows_to_dataframe(rows)


def get_recruiter_filters():
    """
    Fetch distinct values for recruiter-related filter dropdowns.

    Returns:
        dict: {'companies': [...], 'industries': [...], 'cities': [...], 'statuses': [...]}
    """
    companies = [r[0] for r in run_query("SELECT DISTINCT company FROM Recruiters ORDER BY company")]
    industries = [r[0] for r in run_query("SELECT DISTINCT industry FROM Recruiters ORDER BY industry")]
    cities = [r[0] for r in run_query("SELECT DISTINCT city FROM Recruiters ORDER BY city")]
    statuses = [r[0] for r in run_query("SELECT DISTINCT status FROM Recruiters ORDER BY status")]
    return {
        "companies": companies,
        "industries": industries,
        "cities": cities,
        "statuses": statuses,
    }


def get_jobs_by_recruiter():
    """Total job count grouped by recruiter."""
    rows = run_query(get_query("jobs_by_recruiter"))
    return rows_to_dataframe(rows)
