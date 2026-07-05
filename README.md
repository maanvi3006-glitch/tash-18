# PlaceMux — Admin Console & Review Queue

**Task 18 · Data Analyst · Phase 2 · Week 5**
Focus: *Build Top-Recruiter Views with an Admin Console and Review Queue.*

## 1. Project Overview

PlaceMux is a simulated recruitment-platform back office. This module gives
platform administrators a single place to:

- Monitor recruiter and hiring activity across the platform
- Review and approve/reject pending recruiter and company registrations
- Identify top-performing recruiters across multiple ranking dimensions
- Explore recruiter, job, application, and placement data visually and via SQL

The project is built with **Python, SQLite, Pandas, Streamlit, Plotly, and
Faker**, following a modular architecture that separates data generation,
database access, business logic, and presentation.

## 2. Folder Structure

```
placemux/
│
├── create_database.py        # Initializes SQLite DB from sql/schema.sql
├── generate_data.py          # Populates DB with realistic fake data (Faker)
├── database.py                # Centralized DB connection + query helpers
├── requirements.txt
├── README.md
│
├── data/
│   └── placemux.db            # SQLite database file (created at runtime)
│
├── sql/
│   ├── schema.sql              # DDL for all 7 tables + indexes
│   └── queries.sql             # Named, reusable SQL queries
│
├── modules/                    # Business logic layer
│   ├── recruiter.py             # Recruiter analytics & top-recruiter queries
│   ├── review_queue.py          # Review queue approve/reject workflow
│   ├── admin.py                 # Admin dashboard KPIs & approvals
│   ├── analytics.py             # Aggregations feeding Plotly charts
│   └── utils.py                 # Query loader, CSV export, filter helpers
│
├── dashboard/                   # Streamlit presentation layer
│   ├── app.py                    # Main entry point + sidebar navigation
│   ├── recruiter_dashboard.py    # Recruiter Analytics & Top Recruiters pages
│   ├── admin_console.py          # Admin Console page
│   ├── review_queue.py           # Review Queue page
│   ├── analytics_dashboard.py    # Analytics Dashboard page (Plotly charts)
│   └── charts.py                 # Reusable Plotly chart builders
│
└── assets/                       # Static assets (icons/screenshots, if any)
```

## 3. Database Schema

| Table | Purpose |
|---|---|
| `Recruiters` | Recruiter profiles and approval status |
| `Companies` | Company registrations and verification status |
| `Jobs` | Job postings linked to a company and recruiter |
| `Candidates` | Candidate profiles |
| `Applications` | Candidate applications to jobs, with pipeline status |
| `ReviewQueue` | Pending/approved/rejected recruiter & company submissions |
| `RecruiterPerformance` | Per-recruiter hiring performance metrics |

Full column definitions and constraints are in `sql/schema.sql`.

## 4. Installation

**Prerequisites:** Python 3.9+

```bash
# 1. Navigate into the project folder
cd placemux

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 5. How to Run

### Step 1 — Initialize the database

```bash
python create_database.py
```

This drops any existing `data/placemux.db` and recreates all 7 tables
(plus indexes) from `sql/schema.sql`.

### Step 2 — Generate fake data

```bash
python generate_data.py
```

This uses Faker to populate:

- 300 Recruiters
- 200 Companies
- 800 Jobs
- 3,000 Candidates
- 10,000 Applications
- 400 Review Queue items
- 300 Recruiter Performance records

### Step 3 — Launch the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

Then open the local URL Streamlit prints (typically `http://localhost:8501`).

## 6. Features

### Sidebar Navigation
- **Dashboard** — platform-wide KPI overview
- **Recruiter Analytics** — searchable/filterable recruiter table with export
- **Top Recruiters** — Top-10 leaderboards (placement rate, jobs posted, offers,
  conversion rate, activity), sortable and filterable by company/industry/city/status
- **Admin Console** — KPI cards plus one-click approve/reject for pending
  recruiters and companies
- **Review Queue** — interactive queue with filters (status, type, date range)
  and inline approve/reject actions that cascade to the underlying entity
- **SQL Explorer** — run ad-hoc, read-only `SELECT` queries against the database

### Admin Dashboard KPIs
Total Recruiters · Active Recruiters · Pending Recruiter Approvals ·
Verified Companies · Pending Reviews · Rejected Applications · Total Jobs ·
Total Placements · Average Placement Rate

### Analytics Dashboard (Plotly)
Recruiter Performance Leaderboard · Placement Rate by Recruiter ·
Jobs Posted by Company · Applications by Status · Review Queue Status
Distribution · Company Verification Status · Monthly Recruiter Registrations ·
Hiring Funnel

### Export Features
- Export recruiter analytics to CSV
- Export review queue to CSV
- Export recruiter leaderboard to CSV

## 7. Screenshots Placeholder

> Add screenshots of the Dashboard, Top Recruiters, Admin Console, Review
> Queue, and Analytics Dashboard pages here after running the app locally.

```
assets/screenshot-dashboard.png
assets/screenshot-top-recruiters.png
assets/screenshot-admin-console.png
assets/screenshot-review-queue.png
assets/screenshot-analytics.png
```

## 8. Notes

- Re-running `create_database.py` will wipe and recreate the schema —
  run `generate_data.py` again afterward to repopulate it.
- All SQL used by the app is centralized in `sql/queries.sql` and loaded
  via `modules/utils.get_query()`, so queries can be edited without
  touching Python code.
- The Review Queue's approve/reject actions update both the `ReviewQueue`
  row and the underlying `Recruiters`/`Companies` row in a single
  transaction-like operation (see `modules/review_queue.update_review_status`).
