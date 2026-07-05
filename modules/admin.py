"""
modules/admin.py
------------------
Business logic for the Admin Console: dashboard summary metrics and
recruiter/company approval management.
"""

from database import run_query, execute_write
from modules.utils import get_query, rows_to_dataframe


def get_dashboard_summary():
    """
    Fetch top-level KPI metrics for the Admin Dashboard.

    Returns:
        dict: Summary metrics (total recruiters, active recruiters, etc.)
    """
    rows = run_query(get_query("admin_dashboard_summary"))
    if not rows:
        return {}
    return dict(rows[0])


def get_pending_recruiter_approvals():
    """Fetch recruiters awaiting approval."""
    rows = run_query(get_query("pending_recruiter_approvals"))
    return rows_to_dataframe(rows)


def get_pending_company_verifications():
    """Fetch companies awaiting verification."""
    rows = run_query(get_query("pending_company_verifications"))
    return rows_to_dataframe(rows)


def approve_recruiter(recruiter_id):
    """Directly approve a recruiter (sets status to Active)."""
    execute_write("UPDATE Recruiters SET status = 'Active' WHERE recruiter_id = ?", (recruiter_id,))


def reject_recruiter(recruiter_id):
    """Directly reject a recruiter (sets status to Rejected)."""
    execute_write("UPDATE Recruiters SET status = 'Rejected' WHERE recruiter_id = ?", (recruiter_id,))


def approve_company(company_id):
    """Directly verify a company (sets verification_status to Verified)."""
    execute_write("UPDATE Companies SET verification_status = 'Verified' WHERE company_id = ?", (company_id,))


def reject_company(company_id):
    """Directly reject a company (sets verification_status to Rejected)."""
    execute_write("UPDATE Companies SET verification_status = 'Rejected' WHERE company_id = ?", (company_id,))


def get_company_verification_distribution():
    """Fetch counts of companies grouped by verification status."""
    rows = run_query(get_query("company_verification_distribution"))
    return rows_to_dataframe(rows)


def get_all_companies():
    """Fetch every company record."""
    rows = run_query("SELECT * FROM Companies ORDER BY submitted_date DESC")
    return rows_to_dataframe(rows)
