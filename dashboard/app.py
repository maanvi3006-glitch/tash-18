"""
dashboard/app.py
-------------------
Main Streamlit entry point for the PlaceMux Admin Console & Review Queue.

Run with:
    streamlit run dashboard/app.py

Provides sidebar navigation across:
    - Dashboard (Admin KPIs overview)
    - Recruiter Analytics
    - Top Recruiters
    - Admin Console
    - Review Queue
    - SQL Explorer
"""

import os
import sys

import pandas as pd
import streamlit as st

# Ensure the project root is on sys.path so `modules` and `database` are
# importable regardless of the working directory Streamlit is launched from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database import DB_PATH, database_exists, get_connection  # noqa: E402
from dashboard import admin_console, analytics_dashboard, recruiter_dashboard, review_queue  # noqa: E402
from modules import admin as admin_module  # noqa: E402

st.set_page_config(
    page_title="PlaceMux Admin Console",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_dashboard_overview():
    """Render the top-level 'Dashboard' page with headline KPIs."""
    st.header("🧭 PlaceMux Admin Dashboard")
    st.caption("A birds-eye view of recruiter activity, approvals, and placements.")

    summary = admin_module.get_dashboard_summary()

    row1 = st.columns(3)
    row1[0].metric("Total Recruiters", summary.get("total_recruiters", 0))
    row1[1].metric("Active Recruiters", summary.get("active_recruiters", 0))
    row1[2].metric("Pending Recruiter Approvals", summary.get("pending_recruiter_approvals", 0))

    row2 = st.columns(3)
    row2[0].metric("Verified Companies", summary.get("verified_companies", 0))
    row2[1].metric("Pending Reviews", summary.get("pending_reviews", 0))
    row2[2].metric("Rejected Applications", summary.get("rejected_applications", 0))

    row3 = st.columns(3)
    row3[0].metric("Total Jobs", summary.get("total_jobs", 0))
    row3[1].metric("Total Placements", summary.get("total_placements", 0))
    row3[2].metric("Avg Placement Rate", f"{summary.get('avg_placement_rate', 0)}%")

    st.divider()
    st.info(
        "Use the sidebar to explore Recruiter Analytics, Top Recruiter leaderboards, "
        "the Admin Console approval workflow, the interactive Review Queue, "
        "or run ad-hoc queries in the SQL Explorer."
    )


def render_sql_explorer():
    """Render a simple, safe, read-only SQL Explorer page."""
    st.header("🧮 SQL Explorer")
    st.caption("Run read-only SQL queries directly against the PlaceMux database.")

    default_query = "SELECT * FROM Recruiters LIMIT 20;"
    query_text = st.text_area("Enter a SQL SELECT query:", value=default_query, height=140)

    if st.button("▶️ Run Query"):
        normalized = query_text.strip().lower()
        if not normalized.startswith("select"):
            st.error("Only SELECT queries are allowed in the SQL Explorer.")
        else:
            try:
                conn = get_connection()
                result_df = pd.read_sql_query(query_text, conn)
                conn.close()
                st.success(f"Query returned {len(result_df)} rows.")
                st.dataframe(result_df, use_container_width=True, hide_index=True)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Query failed: {exc}")

    with st.expander("💡 Example queries"):
        st.code(
            "SELECT status, COUNT(*) FROM Recruiters GROUP BY status;\n"
            "SELECT * FROM ReviewQueue WHERE review_status = 'Pending';\n"
            "SELECT r.name, p.placement_rate FROM Recruiters r "
            "JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id "
            "ORDER BY p.placement_rate DESC LIMIT 10;",
            language="sql",
        )


def main():
    """Application entry point: sidebar navigation and page routing."""
    st.sidebar.title("🧭 PlaceMux")
    st.sidebar.caption("Admin Console & Review Queue")

    if not database_exists():
        st.error(
            f"Database not found at `{DB_PATH}`.\n\n"
            "Please run the following commands first:\n\n"
            "```\npython create_database.py\npython generate_data.py\n```"
        )
        st.stop()

    page = st.sidebar.radio(
        "Navigate",
        [
            "Dashboard",
            "Recruiter Analytics",
            "Top Recruiters",
            "Admin Console",
            "Review Queue",
            "SQL Explorer",
        ],
    )

    st.sidebar.divider()
    st.sidebar.caption("PlaceMux · Task 18 · Admin Console & Review Queue")

    if page == "Dashboard":
        render_dashboard_overview()
    elif page == "Recruiter Analytics":
        recruiter_dashboard.render_recruiter_analytics()
    elif page == "Top Recruiters":
        recruiter_dashboard.render_top_recruiters()
    elif page == "Admin Console":
        admin_console.render()
    elif page == "Review Queue":
        review_queue.render()
    elif page == "SQL Explorer":
        render_sql_explorer()


if __name__ == "__main__":
    main()
