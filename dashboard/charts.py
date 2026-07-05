"""
dashboard/charts.py
----------------------
Reusable Plotly chart-building functions for the Analytics Dashboard.
Each function accepts a pandas DataFrame (or dict) and returns a
plotly.graph_objects Figure ready to be passed to st.plotly_chart().
"""

import plotly.express as px
import plotly.graph_objects as go

# A consistent color palette used across all charts.
COLOR_SEQUENCE = px.colors.qualitative.Set2


def recruiter_leaderboard_chart(df, top_n=10):
    """Horizontal bar chart: top recruiters ranked by placement rate."""
    if df.empty:
        return go.Figure()
    top_df = df.sort_values("placement_rate", ascending=False).head(top_n)
    fig = px.bar(
        top_df.sort_values("placement_rate"),
        x="placement_rate",
        y="name",
        orientation="h",
        color="placement_rate",
        color_continuous_scale="Blues",
        title=f"Top {top_n} Recruiters - Performance Leaderboard",
        labels={"placement_rate": "Placement Rate (%)", "name": "Recruiter"},
        hover_data=["company", "industry", "hires", "jobs_posted"],
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig


def placement_rate_by_recruiter_chart(df):
    """Bar chart: placement rate distribution across recruiters."""
    if df.empty:
        return go.Figure()
    fig = px.bar(
        df,
        x="name",
        y="placement_rate",
        color="industry",
        title="Placement Rate by Recruiter",
        labels={"placement_rate": "Placement Rate (%)", "name": "Recruiter"},
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig.update_layout(xaxis_tickangle=-45, showlegend=True)
    return fig


def jobs_posted_by_company_chart(df, top_n=15):
    """Bar chart: number of jobs posted per company (top N)."""
    if df.empty:
        return go.Figure()
    top_df = df.sort_values("total_jobs", ascending=False).head(top_n)
    fig = px.bar(
        top_df,
        x="company_name",
        y="total_jobs",
        title=f"Jobs Posted by Company (Top {top_n})",
        labels={"total_jobs": "Total Jobs", "company_name": "Company"},
        color="total_jobs",
        color_continuous_scale="Teal",
    )
    fig.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
    return fig


def applications_by_status_chart(df):
    """Pie chart: applications broken down by status."""
    if df.empty:
        return go.Figure()
    fig = px.pie(
        df,
        names="status",
        values="total",
        title="Applications by Status",
        color_discrete_sequence=COLOR_SEQUENCE,
        hole=0.35,
    )
    return fig


def review_queue_status_chart(df):
    """Pie chart: review queue items broken down by status."""
    if df.empty:
        return go.Figure()
    fig = px.pie(
        df,
        names="review_status",
        values="total",
        title="Review Queue Status Distribution",
        color_discrete_sequence=COLOR_SEQUENCE,
        hole=0.35,
    )
    return fig


def company_verification_chart(df):
    """Donut chart: companies broken down by verification status."""
    if df.empty:
        return go.Figure()
    fig = px.pie(
        df,
        names="verification_status",
        values="total",
        title="Company Verification Status",
        color_discrete_sequence=COLOR_SEQUENCE,
        hole=0.45,
    )
    return fig


def monthly_registrations_chart(df):
    """Line chart: recruiter registrations over time."""
    if df.empty:
        return go.Figure()
    fig = px.line(
        df,
        x="month",
        y="registrations",
        markers=True,
        title="Monthly Recruiter Registrations",
        labels={"month": "Month", "registrations": "New Recruiters"},
    )
    fig.update_traces(line_color="#2E86AB")
    return fig


def hiring_funnel_chart(funnel_dict):
    """Funnel chart: overall hiring pipeline from applied to hired."""
    if not funnel_dict:
        return go.Figure()
    stages = ["Applied", "Shortlisted", "Interviewed", "Offered", "Hired"]
    values = [
        funnel_dict.get("applied", 0),
        funnel_dict.get("shortlisted", 0),
        funnel_dict.get("interviewed", 0),
        funnel_dict.get("offered", 0),
        funnel_dict.get("hired", 0),
    ]
    fig = go.Figure(
        go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker={"color": COLOR_SEQUENCE[: len(stages)]},
        )
    )
    fig.update_layout(title="Hiring Funnel")
    return fig
