-- =====================================================================
-- PlaceMux Reusable SQL Queries
-- =====================================================================

-- -----------------------------------------------------------------
-- 1. TOP RECRUITERS BY PLACEMENT RATE
-- -----------------------------------------------------------------
-- name: top_recruiters_by_placement_rate
SELECT
    r.recruiter_id,
    r.name,
    r.company,
    r.industry,
    r.city,
    r.status,
    p.jobs_posted,
    p.applications_received,
    p.interviews,
    p.offers_made,
    p.hires,
    p.placement_rate
FROM Recruiters r
JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id
ORDER BY p.placement_rate DESC
LIMIT 10;

-- -----------------------------------------------------------------
-- 2. TOP RECRUITERS BY JOBS POSTED
-- -----------------------------------------------------------------
-- name: top_recruiters_by_jobs_posted
SELECT
    r.recruiter_id, r.name, r.company, r.industry, r.city,
    p.jobs_posted, p.placement_rate
FROM Recruiters r
JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id
ORDER BY p.jobs_posted DESC
LIMIT 10;

-- -----------------------------------------------------------------
-- 3. TOP RECRUITERS BY OFFERS MADE
-- -----------------------------------------------------------------
-- name: top_recruiters_by_offers
SELECT
    r.recruiter_id, r.name, r.company, r.industry, r.city,
    p.offers_made, p.hires, p.placement_rate
FROM Recruiters r
JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id
ORDER BY p.offers_made DESC
LIMIT 10;

-- -----------------------------------------------------------------
-- 4. TOP RECRUITERS BY CANDIDATE CONVERSION RATE (hires/applications)
-- -----------------------------------------------------------------
-- name: top_recruiters_by_conversion
SELECT
    r.recruiter_id, r.name, r.company, r.industry, r.city,
    p.applications_received, p.hires,
    ROUND(CAST(p.hires AS REAL) / NULLIF(p.applications_received, 0) * 100, 2) AS conversion_rate
FROM Recruiters r
JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id
ORDER BY conversion_rate DESC
LIMIT 10;

-- -----------------------------------------------------------------
-- 5. MOST ACTIVE RECRUITERS (by applications received)
-- -----------------------------------------------------------------
-- name: most_active_recruiters
SELECT
    r.recruiter_id, r.name, r.company, r.industry, r.city,
    p.applications_received, p.interviews, p.jobs_posted
FROM Recruiters r
JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id
ORDER BY p.applications_received DESC
LIMIT 10;

-- -----------------------------------------------------------------
-- 6. PENDING RECRUITER APPROVALS
-- -----------------------------------------------------------------
-- name: pending_recruiter_approvals
SELECT recruiter_id, name, company, industry, city, joined_date
FROM Recruiters
WHERE status = 'Pending'
ORDER BY joined_date DESC;

-- -----------------------------------------------------------------
-- 7. PENDING COMPANY VERIFICATIONS
-- -----------------------------------------------------------------
-- name: pending_company_verifications
SELECT company_id, company_name, industry, size, submitted_date
FROM Companies
WHERE verification_status = 'Pending'
ORDER BY submitted_date DESC;

-- -----------------------------------------------------------------
-- 8. FULL RECRUITER PERFORMANCE
-- -----------------------------------------------------------------
-- name: recruiter_performance_full
SELECT
    r.recruiter_id, r.name, r.company, r.industry, r.city, r.status,
    p.jobs_posted, p.applications_received, p.interviews,
    p.offers_made, p.hires, p.placement_rate
FROM Recruiters r
JOIN RecruiterPerformance p ON r.recruiter_id = p.recruiter_id;

-- -----------------------------------------------------------------
-- 9. REVIEW QUEUE (ALL / FILTERABLE)
-- -----------------------------------------------------------------
-- name: review_queue_all
SELECT
    review_id, entity_type, entity_id, submitted_by,
    submission_date, review_status, reviewer, review_date, comments
FROM ReviewQueue
ORDER BY submission_date DESC;

-- name: review_queue_pending
SELECT
    review_id, entity_type, entity_id, submitted_by,
    submission_date, review_status, reviewer, review_date, comments
FROM ReviewQueue
WHERE review_status = 'Pending'
ORDER BY submission_date DESC;

-- -----------------------------------------------------------------
-- 10. PLACEMENT STATISTICS (OVERALL)
-- -----------------------------------------------------------------
-- name: placement_statistics
SELECT
    SUM(hires) AS total_placements,
    SUM(offers_made) AS total_offers,
    SUM(applications_received) AS total_applications,
    ROUND(AVG(placement_rate), 2) AS avg_placement_rate
FROM RecruiterPerformance;

-- -----------------------------------------------------------------
-- 11. JOBS BY RECRUITER
-- -----------------------------------------------------------------
-- name: jobs_by_recruiter
SELECT
    r.recruiter_id, r.name, COUNT(j.job_id) AS total_jobs
FROM Recruiters r
LEFT JOIN Jobs j ON r.recruiter_id = j.recruiter_id
GROUP BY r.recruiter_id, r.name
ORDER BY total_jobs DESC;

-- -----------------------------------------------------------------
-- 12. JOBS POSTED BY COMPANY
-- -----------------------------------------------------------------
-- name: jobs_by_company
SELECT
    c.company_id, c.company_name, COUNT(j.job_id) AS total_jobs
FROM Companies c
LEFT JOIN Jobs j ON c.company_id = j.company_id
GROUP BY c.company_id, c.company_name
ORDER BY total_jobs DESC;

-- -----------------------------------------------------------------
-- 13. COMPANY VERIFICATION STATUS DISTRIBUTION
-- -----------------------------------------------------------------
-- name: company_verification_distribution
SELECT verification_status, COUNT(*) AS total
FROM Companies
GROUP BY verification_status;

-- -----------------------------------------------------------------
-- 14. MONTHLY RECRUITER REGISTRATIONS
-- -----------------------------------------------------------------
-- name: monthly_recruiter_registrations
SELECT
    strftime('%Y-%m', joined_date) AS month,
    COUNT(*) AS registrations
FROM Recruiters
GROUP BY month
ORDER BY month;

-- -----------------------------------------------------------------
-- 15. APPLICATIONS BY STATUS
-- -----------------------------------------------------------------
-- name: applications_by_status
SELECT status, COUNT(*) AS total
FROM Applications
GROUP BY status;

-- -----------------------------------------------------------------
-- 16. REVIEW QUEUE STATUS DISTRIBUTION
-- -----------------------------------------------------------------
-- name: review_queue_status_distribution
SELECT review_status, COUNT(*) AS total
FROM ReviewQueue
GROUP BY review_status;

-- -----------------------------------------------------------------
-- 17. HIRING FUNNEL (OVERALL)
-- -----------------------------------------------------------------
-- name: hiring_funnel
SELECT
    (SELECT COUNT(*) FROM Applications) AS applied,
    (SELECT COUNT(*) FROM Applications WHERE status = 'Shortlisted') AS shortlisted,
    (SELECT COUNT(*) FROM Applications WHERE status = 'Interviewed') AS interviewed,
    (SELECT COUNT(*) FROM Applications WHERE status = 'Offered') AS offered,
    (SELECT COUNT(*) FROM Applications WHERE status = 'Hired') AS hired;

-- -----------------------------------------------------------------
-- 18. ADMIN DASHBOARD SUMMARY METRICS
-- -----------------------------------------------------------------
-- name: admin_dashboard_summary
SELECT
    (SELECT COUNT(*) FROM Recruiters) AS total_recruiters,
    (SELECT COUNT(*) FROM Recruiters WHERE status = 'Active') AS active_recruiters,
    (SELECT COUNT(*) FROM Recruiters WHERE status = 'Pending') AS pending_recruiter_approvals,
    (SELECT COUNT(*) FROM Companies WHERE verification_status = 'Verified') AS verified_companies,
    (SELECT COUNT(*) FROM ReviewQueue WHERE review_status = 'Pending') AS pending_reviews,
    (SELECT COUNT(*) FROM Applications WHERE status = 'Rejected') AS rejected_applications,
    (SELECT COUNT(*) FROM Jobs) AS total_jobs,
    (SELECT SUM(hires) FROM RecruiterPerformance) AS total_placements,
    (SELECT ROUND(AVG(placement_rate), 2) FROM RecruiterPerformance) AS avg_placement_rate;
