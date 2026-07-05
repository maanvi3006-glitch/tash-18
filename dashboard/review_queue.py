"""
dashboard/review_queue.py
-----------------------------
Streamlit page: Interactive Review Queue.

Lets admins view, filter, and act on ReviewQueue submissions
(Recruiter and Company registrations).
"""

import datetime

import streamlit as st

from modules import review_queue as review_queue_module
from modules.utils import apply_date_range_filter, apply_exact_filter, dataframe_to_csv_bytes


def render():
    """Render the Review Queue page."""
    st.header("📥 Review Queue")
    st.caption("Review, approve, or reject pending recruiter and company submissions.")

    df = review_queue_module.get_all_review_items()
    filters = review_queue_module.get_review_queue_filters()

    # --- Filters ---
    with st.expander("🔍 Filters", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            status_filter = st.selectbox("Review Status", ["All"] + filters["statuses"], key="rq_status")
        with c2:
            type_filter = st.selectbox("Review Type", ["All"] + filters["entity_types"], key="rq_type")
        with c3:
            date_range = st.date_input(
                "Submission Date Range",
                value=(datetime.date(2021, 1, 1), datetime.date.today()),
                key="rq_daterange",
            )

    filtered_df = df.copy()
    filtered_df = apply_exact_filter(filtered_df, "review_status", status_filter)
    filtered_df = apply_exact_filter(filtered_df, "entity_type", type_filter)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        filtered_df = apply_date_range_filter(filtered_df, "submission_date", date_range[0], date_range[1])

    # --- Summary ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Items", len(filtered_df))
    m2.metric("Pending", int((filtered_df["review_status"] == "Pending").sum()) if not filtered_df.empty else 0)
    m3.metric("Reviewed", int((filtered_df["review_status"] != "Pending").sum()) if not filtered_df.empty else 0)

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    st.download_button(
        label="⬇️ Export Review Queue to CSV",
        data=dataframe_to_csv_bytes(filtered_df),
        file_name="review_queue.csv",
        mime="text/csv",
    )

    st.divider()

    # --- Actionable pending items ---
    st.subheader("⚡ Take Action on Pending Items")
    pending_df = review_queue_module.get_pending_review_items()

    if pending_df.empty:
        st.info("No pending review items remain.")
        return

    for _, row in pending_df.iterrows():
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.markdown(
                f"**Review #{row['review_id']}** — {row['entity_type']} (ID {row['entity_id']})  \n"
                f"Submitted by {row['submitted_by']} on {row['submission_date']}"
            )
            if c2.button("✅ Approve", key=f"rq_approve_{row['review_id']}"):
                review_queue_module.approve_item(row["review_id"])
                st.success(f"Approved review #{row['review_id']}")
                st.rerun()
            if c3.button("❌ Reject", key=f"rq_reject_{row['review_id']}"):
                review_queue_module.reject_item(row["review_id"])
                st.warning(f"Rejected review #{row['review_id']}")
                st.rerun()
