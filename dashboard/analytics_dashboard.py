"""
dashboard/analytics_dashboard.py
------------------------------------
Streamlit page: Analytics Dashboard.

Renders all Plotly visualizations required by Task 18: recruiter
performance, jobs, applications, review queue, company verification,
registrations over time, and the hiring funnel.
"""

import streamlit as st

from dashboard import charts
from modules import analytics as analytics_module


def render():
    """Render the Analytics Dashboard page."""
    st.header("📈 Analytics Dashboard")
    st.caption("Visual insights into recruiter performance, hiring activity, and platform health.")

    leaderboard_df = analytics_module.get_recruiter_performance_leaderboard()
    placement_df = analytics_module.get_placement_rate_by_recruiter(limit=15)
    jobs_by_company_df = analytics_module.get_jobs_posted_by_company()
    applications_status_df = analytics_module.get_applications_by_status()
    review_status_df = analytics_module.get_review_queue_status_distribution()
    company_verification_df = analytics_module.get_company_verification_status()
    monthly_registrations_df = analytics_module.get_monthly_recruiter_registrations()
    funnel_dict = analytics_module.get_hiring_funnel()

    # Row 1: Leaderboard + Placement rate
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts.recruiter_leaderboard_chart(leaderboard_df), use_container_width=True)
    with col2:
        st.plotly_chart(charts.placement_rate_by_recruiter_chart(placement_df), use_container_width=True)

    # Row 2: Jobs by company + Applications by status
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(charts.jobs_posted_by_company_chart(jobs_by_company_df), use_container_width=True)
    with col4:
        st.plotly_chart(charts.applications_by_status_chart(applications_status_df), use_container_width=True)

    # Row 3: Review queue status + Company verification
    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(charts.review_queue_status_chart(review_status_df), use_container_width=True)
    with col6:
        st.plotly_chart(charts.company_verification_chart(company_verification_df), use_container_width=True)

    # Row 4: Monthly registrations + Hiring funnel
    col7, col8 = st.columns(2)
    with col7:
        st.plotly_chart(charts.monthly_registrations_chart(monthly_registrations_df), use_container_width=True)
    with col8:
        st.plotly_chart(charts.hiring_funnel_chart(funnel_dict), use_container_width=True)

    st.divider()

    # Placement statistics summary
    st.subheader("📌 Placement Statistics Summary")
    stats = analytics_module.get_placement_statistics()
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Placements", stats.get("total_placements", 0))
    s2.metric("Total Offers", stats.get("total_offers", 0))
    s3.metric("Total Applications", stats.get("total_applications", 0))
    s4.metric("Avg Placement Rate", f"{stats.get('avg_placement_rate', 0)}%")
