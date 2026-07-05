"""
dashboard/recruiter_dashboard.py
-----------------------------------
Streamlit page: Recruiter Analytics and Top Recruiter Views.

Contains two sections (both rendered based on sidebar selection in
app.py): a filterable full recruiter analytics table, and the
Top-10 recruiter leaderboards required by Task 18.
"""

import streamlit as st

from modules import recruiter as recruiter_module
from modules.utils import apply_exact_filter, apply_text_filter, dataframe_to_csv_bytes


def render_recruiter_analytics():
    """Render the 'Recruiter Analytics' page: full searchable/filterable table."""
    st.header("📊 Recruiter Analytics")
    st.caption("Search, filter, and export the complete recruiter dataset.")

    df = recruiter_module.get_all_recruiters()
    filters = recruiter_module.get_recruiter_filters()

    # --- Search & Filter controls ---
    with st.expander("🔍 Search & Filters", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            name_search = st.text_input("Recruiter Name", key="ra_name")
        with col2:
            company_filter = st.selectbox("Company", ["All"] + filters["companies"], key="ra_company")
        with col3:
            industry_filter = st.selectbox("Industry", ["All"] + filters["industries"], key="ra_industry")
        with col4:
            city_filter = st.selectbox("City", ["All"] + filters["cities"], key="ra_city")

        status_filter = st.selectbox("Status", ["All"] + filters["statuses"], key="ra_status")

    filtered_df = df.copy()
    filtered_df = apply_text_filter(filtered_df, "name", name_search)
    filtered_df = apply_exact_filter(filtered_df, "company", company_filter)
    filtered_df = apply_exact_filter(filtered_df, "industry", industry_filter)
    filtered_df = apply_exact_filter(filtered_df, "city", city_filter)
    filtered_df = apply_exact_filter(filtered_df, "status", status_filter)

    # --- Summary metrics for the filtered set ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Recruiters Shown", len(filtered_df))
    m2.metric("Total Jobs Posted", int(filtered_df["jobs_posted"].sum()) if not filtered_df.empty else 0)
    m3.metric("Total Hires", int(filtered_df["hires"].sum()) if not filtered_df.empty else 0)
    avg_rate = filtered_df["placement_rate"].mean() if not filtered_df.empty else 0
    m4.metric("Avg Placement Rate", f"{avg_rate:.2f}%")

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    st.download_button(
        label="⬇️ Export Recruiter Analytics to CSV",
        data=dataframe_to_csv_bytes(filtered_df),
        file_name="recruiter_analytics.csv",
        mime="text/csv",
    )


def render_top_recruiters():
    """Render the 'Top Recruiters' page: leaderboards required by Task 18."""
    st.header("🏆 Top Recruiter Views")
    st.caption("Top-performing recruiters across multiple performance dimensions.")

    tab_labels = [
        "Highest Placement Rate",
        "Most Jobs Posted",
        "Highest Offers Made",
        "Highest Conversion Rate",
        "Most Active",
    ]
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        df = recruiter_module.get_top_recruiters_by_placement_rate()
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[1]:
        df = recruiter_module.get_top_recruiters_by_jobs_posted()
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[2]:
        df = recruiter_module.get_top_recruiters_by_offers()
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[3]:
        df = recruiter_module.get_top_recruiters_by_conversion()
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[4]:
        df = recruiter_module.get_most_active_recruiters()
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    leaderboard_df = recruiter_module.get_top_recruiters_by_placement_rate()
    st.download_button(
        label="⬇️ Export Top Recruiter Leaderboard to CSV",
        data=dataframe_to_csv_bytes(leaderboard_df),
        file_name="top_recruiters_leaderboard.csv",
        mime="text/csv",
    )
