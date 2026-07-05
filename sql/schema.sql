-- =====================================================================
-- PlaceMux Database Schema
-- Admin Console & Review Queue - Task 18
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Recruiters
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS Recruiters;
CREATE TABLE Recruiters (
    recruiter_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT NOT NULL,
    company           TEXT NOT NULL,
    email             TEXT NOT NULL UNIQUE,
    industry          TEXT NOT NULL,
    city              TEXT NOT NULL,
    experience_years  INTEGER NOT NULL,
    status            TEXT NOT NULL CHECK (status IN ('Active', 'Pending', 'Suspended', 'Rejected')),
    joined_date       TEXT NOT NULL
);

-- ---------------------------------------------------------------------
-- Companies
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS Companies;
CREATE TABLE Companies (
    company_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name         TEXT NOT NULL,
    industry             TEXT NOT NULL,
    size                 TEXT NOT NULL CHECK (size IN ('Startup', 'Small', 'Medium', 'Large', 'Enterprise')),
    verification_status  TEXT NOT NULL CHECK (verification_status IN ('Verified', 'Pending', 'Rejected')),
    submitted_date       TEXT NOT NULL
);

-- ---------------------------------------------------------------------
-- Jobs
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS Jobs;
CREATE TABLE Jobs (
    job_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id    INTEGER NOT NULL,
    recruiter_id  INTEGER NOT NULL,
    title         TEXT NOT NULL,
    location      TEXT NOT NULL,
    salary        INTEGER NOT NULL,
    posted_date   TEXT NOT NULL,
    status        TEXT NOT NULL CHECK (status IN ('Open', 'Closed', 'On Hold')),
    FOREIGN KEY (company_id) REFERENCES Companies(company_id),
    FOREIGN KEY (recruiter_id) REFERENCES Recruiters(recruiter_id)
);

-- ---------------------------------------------------------------------
-- Candidates
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS Candidates;
CREATE TABLE Candidates (
    candidate_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    skills        TEXT NOT NULL,
    experience    INTEGER NOT NULL,
    city          TEXT NOT NULL
);

-- ---------------------------------------------------------------------
-- Applications
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS Applications;
CREATE TABLE Applications (
    application_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id    INTEGER NOT NULL,
    job_id          INTEGER NOT NULL,
    applied_date    TEXT NOT NULL,
    status          TEXT NOT NULL CHECK (status IN ('Applied', 'Shortlisted', 'Interviewed', 'Offered', 'Hired', 'Rejected')),
    FOREIGN KEY (candidate_id) REFERENCES Candidates(candidate_id),
    FOREIGN KEY (job_id) REFERENCES Jobs(job_id)
);

-- ---------------------------------------------------------------------
-- ReviewQueue
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS ReviewQueue;
CREATE TABLE ReviewQueue (
    review_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type      TEXT NOT NULL CHECK (entity_type IN ('Recruiter', 'Company')),
    entity_id        INTEGER NOT NULL,
    submitted_by     TEXT NOT NULL,
    submission_date  TEXT NOT NULL,
    review_status    TEXT NOT NULL CHECK (review_status IN ('Pending', 'Approved', 'Rejected')),
    reviewer         TEXT,
    review_date      TEXT,
    comments         TEXT
);

-- ---------------------------------------------------------------------
-- RecruiterPerformance
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS RecruiterPerformance;
CREATE TABLE RecruiterPerformance (
    performance_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id          INTEGER NOT NULL,
    jobs_posted           INTEGER NOT NULL,
    applications_received INTEGER NOT NULL,
    interviews            INTEGER NOT NULL,
    offers_made           INTEGER NOT NULL,
    hires                 INTEGER NOT NULL,
    placement_rate        REAL NOT NULL,
    FOREIGN KEY (recruiter_id) REFERENCES Recruiters(recruiter_id)
);

-- ---------------------------------------------------------------------
-- Indexes for performance
-- ---------------------------------------------------------------------
CREATE INDEX idx_jobs_recruiter ON Jobs(recruiter_id);
CREATE INDEX idx_jobs_company ON Jobs(company_id);
CREATE INDEX idx_applications_job ON Applications(job_id);
CREATE INDEX idx_applications_candidate ON Applications(candidate_id);
CREATE INDEX idx_reviewqueue_status ON ReviewQueue(review_status);
CREATE INDEX idx_reviewqueue_entity ON ReviewQueue(entity_type, entity_id);
CREATE INDEX idx_performance_recruiter ON RecruiterPerformance(recruiter_id);
CREATE INDEX idx_recruiters_status ON Recruiters(status);
CREATE INDEX idx_companies_verification ON Companies(verification_status);
