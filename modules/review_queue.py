"""
modules/review_queue.py
--------------------------
Business logic for the Review Queue: viewing pending submissions and
approving/rejecting recruiter or company registrations.
"""

from datetime import date

from database import run_query, execute_write
from modules.utils import get_query, rows_to_dataframe


def get_all_review_items():
    """Fetch every review queue item."""
    rows = run_query(get_query("review_queue_all"))
    return rows_to_dataframe(rows)


def get_pending_review_items():
    """Fetch only pending review queue items."""
    rows = run_query(get_query("review_queue_pending"))
    return rows_to_dataframe(rows)


def get_review_item(review_id):
    """Fetch a single review queue item by its ID."""
    rows = run_query("SELECT * FROM ReviewQueue WHERE review_id = ?", (review_id,))
    return rows[0] if rows else None


def update_review_status(review_id, new_status, reviewer, comments=None):
    """
    Update a review queue item's status (Approved/Rejected) and cascade
    the decision to the underlying entity (Recruiter or Company).

    Args:
        review_id (int): The ReviewQueue.review_id to update.
        new_status (str): 'Approved' or 'Rejected'.
        reviewer (str): Name of the admin performing the review.
        comments (str | None): Optional review comments.

    Returns:
        bool: True if the update succeeded.
    """
    item = get_review_item(review_id)
    if item is None:
        return False

    today = date.today().isoformat()

    # Update the ReviewQueue record itself.
    execute_write(
        """UPDATE ReviewQueue
           SET review_status = ?, reviewer = ?, review_date = ?, comments = ?
           WHERE review_id = ?""",
        (new_status, reviewer, today, comments, review_id),
    )

    # Cascade the decision to the underlying entity.
    entity_type = item["entity_type"]
    entity_id = item["entity_id"]

    if entity_type == "Recruiter":
        recruiter_status = "Active" if new_status == "Approved" else "Rejected"
        execute_write(
            "UPDATE Recruiters SET status = ? WHERE recruiter_id = ?",
            (recruiter_status, entity_id),
        )
    elif entity_type == "Company":
        company_status = "Verified" if new_status == "Approved" else "Rejected"
        execute_write(
            "UPDATE Companies SET verification_status = ? WHERE company_id = ?",
            (company_status, entity_id),
        )

    return True


def approve_item(review_id, reviewer="Admin", comments="Approved via Admin Console"):
    """Convenience wrapper to approve a review queue item."""
    return update_review_status(review_id, "Approved", reviewer, comments)


def reject_item(review_id, reviewer="Admin", comments="Rejected via Admin Console"):
    """Convenience wrapper to reject a review queue item."""
    return update_review_status(review_id, "Rejected", reviewer, comments)


def get_review_queue_filters():
    """
    Fetch distinct values for review-queue-related filter dropdowns.

    Returns:
        dict: {'entity_types': [...], 'statuses': [...]}
    """
    entity_types = [r[0] for r in run_query("SELECT DISTINCT entity_type FROM ReviewQueue ORDER BY entity_type")]
    statuses = [r[0] for r in run_query("SELECT DISTINCT review_status FROM ReviewQueue ORDER BY review_status")]
    return {"entity_types": entity_types, "statuses": statuses}
