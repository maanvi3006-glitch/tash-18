"""
dashboard/admin_console.py
------------------------------
Streamlit page: Admin Console.

Displays platform-wide KPIs and allows administrators to directly
approve/reject pending recruiters and companies.
"""

import streamlit as st

from modules import admin as admin_module


def render():
    """Render the Admin Console page."""
    st.header("🛠️ Admin Console")
    st.caption("Monitor platform health and manage recruiter/company approvals.")

    summary = admin_module.get_dashboard_summary()

    # --- KPI metric cards ---
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

    # --- Pending recruiter approvals ---
    st.subheader("👤 Pending Recruiter Approvals")
    pending_recruiters = admin_module.get_pending_recruiter_approvals()

    if pending_recruiters.empty:
        st.info("No recruiters are currently pending approval.")
    else:
        for _, row in pending_recruiters.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(
                    f"**{row['name']}** — {row['company']}  \n"
                    f"{row['industry']} · {row['city']} · Joined {row['joined_date']}"
                )
                if c2.button("✅ Approve", key=f"approve_rec_{row['recruiter_id']}"):
                    admin_module.approve_recruiter(row["recruiter_id"])
                    st.success(f"Approved {row['name']}")
                    st.rerun()
                if c3.button("❌ Reject", key=f"reject_rec_{row['recruiter_id']}"):
                    admin_module.reject_recruiter(row["recruiter_id"])
                    st.warning(f"Rejected {row['name']}")
                    st.rerun()

    st.divider()

    # --- Pending company verifications ---
    st.subheader("🏢 Pending Company Verifications")
    pending_companies = admin_module.get_pending_company_verifications()

    if pending_companies.empty:
        st.info("No companies are currently pending verification.")
    else:
        for _, row in pending_companies.iterrows():
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(
                    f"**{row['company_name']}**  \n"
                    f"{row['industry']} · {row['size']} · Submitted {row['submitted_date']}"
                )
                if c2.button("✅ Verify", key=f"approve_co_{row['company_id']}"):
                    admin_module.approve_company(row["company_id"])
                    st.success(f"Verified {row['company_name']}")
                    st.rerun()
                if c3.button("❌ Reject", key=f"reject_co_{row['company_id']}"):
                    admin_module.reject_company(row["company_id"])
                    st.warning(f"Rejected {row['company_name']}")
                    st.rerun()

    st.divider()

    # --- All companies table ---
    st.subheader("📋 All Companies")
    st.dataframe(admin_module.get_all_companies(), use_container_width=True, hide_index=True)
