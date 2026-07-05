"""
generate_data.py
------------------
Populates the PlaceMux SQLite database with realistic fake data using
the Faker library.

Generates:
    300   Recruiters
    200   Companies
    800   Jobs
    3000  Candidates
    10000 Applications
    400   ReviewQueue items
    300   RecruiterPerformance records

Run after create_database.py:

    python create_database.py
    python generate_data.py
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta

from faker import Faker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "placemux.db")

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---------------------------------------------------------------------
# Reference data pools
# ---------------------------------------------------------------------
INDUSTRIES = [
    "Information Technology", "Finance", "Healthcare", "Manufacturing",
    "Retail", "Education", "Telecommunications", "Logistics",
    "Real Estate", "Hospitality", "Energy", "Media & Entertainment",
]

COMPANY_SIZES = ["Startup", "Small", "Medium", "Large", "Enterprise"]
RECRUITER_STATUSES = ["Active", "Active", "Active", "Pending", "Suspended", "Rejected"]
VERIFICATION_STATUSES = ["Verified", "Verified", "Pending", "Rejected"]
JOB_STATUSES = ["Open", "Closed", "On Hold"]
APPLICATION_STATUSES = ["Applied", "Shortlisted", "Interviewed", "Offered", "Hired", "Rejected"]
REVIEW_STATUSES = ["Pending", "Approved", "Rejected"]
ENTITY_TYPES = ["Recruiter", "Company"]

JOB_TITLES = [
    "Software Engineer", "Data Analyst", "Product Manager", "HR Executive",
    "Sales Manager", "Business Analyst", "DevOps Engineer", "QA Engineer",
    "UI/UX Designer", "Marketing Specialist", "Financial Analyst",
    "Operations Manager", "Customer Success Manager", "Data Scientist",
    "Recruiter", "Content Writer", "Network Engineer", "Project Manager",
]

SKILLS_POOL = [
    "Python", "SQL", "Excel", "Java", "React", "Communication",
    "Project Management", "Data Analysis", "Machine Learning", "AWS",
    "Sales", "Negotiation", "Marketing", "Leadership", "C++",
    "Docker", "Kubernetes", "Tableau", "Power BI", "Node.js",
]


def random_date(start_year=2021, end_year=2026):
    """Generate a random ISO-format date string between two years."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 6, 30)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def generate_recruiters(conn, count=300):
    """Generate and insert fake recruiters. Returns list of recruiter_ids."""
    rows = []
    for _ in range(count):
        name = fake.name()
        company = fake.company()
        email = fake.unique.email()
        industry = random.choice(INDUSTRIES)
        city = fake.city()
        experience_years = random.randint(0, 25)
        status = random.choice(RECRUITER_STATUSES)
        joined_date = random_date(2021, 2026)
        rows.append((name, company, email, industry, city, experience_years, status, joined_date))

    conn.executemany(
        """INSERT INTO Recruiters
           (name, company, email, industry, city, experience_years, status, joined_date)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()
    cursor = conn.execute("SELECT recruiter_id FROM Recruiters")
    return [r[0] for r in cursor.fetchall()]


def generate_companies(conn, count=200):
    """Generate and insert fake companies. Returns list of company_ids."""
    rows = []
    for _ in range(count):
        company_name = fake.company()
        industry = random.choice(INDUSTRIES)
        size = random.choice(COMPANY_SIZES)
        verification_status = random.choice(VERIFICATION_STATUSES)
        submitted_date = random_date(2021, 2026)
        rows.append((company_name, industry, size, verification_status, submitted_date))

    conn.executemany(
        """INSERT INTO Companies
           (company_name, industry, size, verification_status, submitted_date)
           VALUES (?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()
    cursor = conn.execute("SELECT company_id FROM Companies")
    return [r[0] for r in cursor.fetchall()]


def generate_jobs(conn, company_ids, recruiter_ids, count=800):
    """Generate and insert fake jobs. Returns list of job_ids."""
    rows = []
    for _ in range(count):
        company_id = random.choice(company_ids)
        recruiter_id = random.choice(recruiter_ids)
        title = random.choice(JOB_TITLES)
        location = fake.city()
        salary = random.randint(30000, 220000)
        posted_date = random_date(2022, 2026)
        status = random.choice(JOB_STATUSES)
        rows.append((company_id, recruiter_id, title, location, salary, posted_date, status))

    conn.executemany(
        """INSERT INTO Jobs
           (company_id, recruiter_id, title, location, salary, posted_date, status)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()
    cursor = conn.execute("SELECT job_id FROM Jobs")
    return [r[0] for r in cursor.fetchall()]


def generate_candidates(conn, count=3000):
    """Generate and insert fake candidates. Returns list of candidate_ids."""
    rows = []
    for _ in range(count):
        name = fake.name()
        skills = ", ".join(random.sample(SKILLS_POOL, k=random.randint(2, 5)))
        experience = random.randint(0, 20)
        city = fake.city()
        rows.append((name, skills, experience, city))

    conn.executemany(
        """INSERT INTO Candidates (name, skills, experience, city)
           VALUES (?, ?, ?, ?)""",
        rows,
    )
    conn.commit()
    cursor = conn.execute("SELECT candidate_id FROM Candidates")
    return [r[0] for r in cursor.fetchall()]


def generate_applications(conn, candidate_ids, job_ids, count=10000):
    """Generate and insert fake applications."""
    rows = []
    for _ in range(count):
        candidate_id = random.choice(candidate_ids)
        job_id = random.choice(job_ids)
        applied_date = random_date(2022, 2026)
        status = random.choice(APPLICATION_STATUSES)
        rows.append((candidate_id, job_id, applied_date, status))

    conn.executemany(
        """INSERT INTO Applications (candidate_id, job_id, applied_date, status)
           VALUES (?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def generate_review_queue(conn, recruiter_ids, company_ids, count=400):
    """Generate and insert fake review queue entries."""
    rows = []
    for _ in range(count):
        entity_type = random.choice(ENTITY_TYPES)
        entity_id = random.choice(recruiter_ids) if entity_type == "Recruiter" else random.choice(company_ids)
        submitted_by = fake.name()
        submission_date = random_date(2022, 2026)
        review_status = random.choice(REVIEW_STATUSES)

        reviewer = None
        review_date = None
        comments = None
        if review_status != "Pending":
            reviewer = fake.name()
            review_date = random_date(2022, 2026)
            comments = random.choice([
                "Documents verified successfully.",
                "Incomplete information provided.",
                "Meets platform compliance standards.",
                "Duplicate submission detected.",
                "Escalated for manual verification.",
                "Approved after background check.",
            ])

        rows.append((entity_type, entity_id, submitted_by, submission_date,
                     review_status, reviewer, review_date, comments))

    conn.executemany(
        """INSERT INTO ReviewQueue
           (entity_type, entity_id, submitted_by, submission_date,
            review_status, reviewer, review_date, comments)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def generate_recruiter_performance(conn, recruiter_ids, count=300):
    """Generate and insert fake recruiter performance records."""
    rows = []
    # Ensure one performance record per recruiter (count should equal len(recruiter_ids)).
    sample_ids = recruiter_ids[:count] if len(recruiter_ids) >= count else recruiter_ids

    for recruiter_id in sample_ids:
        jobs_posted = random.randint(1, 40)
        applications_received = random.randint(jobs_posted * 2, jobs_posted * 50)
        interviews = random.randint(0, applications_received // 3 + 1)
        offers_made = random.randint(0, interviews // 2 + 1) if interviews > 0 else 0
        hires = random.randint(0, offers_made) if offers_made > 0 else 0
        placement_rate = round((hires / jobs_posted) * 100, 2) if jobs_posted > 0 else 0.0

        rows.append((recruiter_id, jobs_posted, applications_received,
                     interviews, offers_made, hires, placement_rate))

    conn.executemany(
        """INSERT INTO RecruiterPerformance
           (recruiter_id, jobs_posted, applications_received, interviews,
            offers_made, hires, placement_rate)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        rows,
    )
    conn.commit()


def generate_all_data():
    """Main entry point: generate and insert all fake data into the database."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. Run 'python create_database.py' first."
        )

    conn = sqlite3.connect(DB_PATH)
    try:
        print("[generate_data] Generating Recruiters...")
        recruiter_ids = generate_recruiters(conn, count=300)

        print("[generate_data] Generating Companies...")
        company_ids = generate_companies(conn, count=200)

        print("[generate_data] Generating Jobs...")
        job_ids = generate_jobs(conn, company_ids, recruiter_ids, count=800)

        print("[generate_data] Generating Candidates...")
        candidate_ids = generate_candidates(conn, count=3000)

        print("[generate_data] Generating Applications...")
        generate_applications(conn, candidate_ids, job_ids, count=10000)

        print("[generate_data] Generating Review Queue items...")
        generate_review_queue(conn, recruiter_ids, company_ids, count=400)

        print("[generate_data] Generating Recruiter Performance records...")
        generate_recruiter_performance(conn, recruiter_ids, count=300)

        print("[generate_data] Data generation complete.")

        # Print row counts for a quick sanity check.
        for table in ["Recruiters", "Companies", "Jobs", "Candidates",
                      "Applications", "ReviewQueue", "RecruiterPerformance"]:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            print(f"  {table}: {cursor.fetchone()[0]} rows")
    finally:
        conn.close()


if __name__ == "__main__":
    generate_all_data()
