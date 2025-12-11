"""
Audit Logging System.
Records all security-relevant actions for compliance and debugging.
"""

from datetime import datetime
from typing import Optional
import logging
import uuid

logger = logging.getLogger(__name__)

# In-memory store for development (replace with database in production)
_audit_logs = []


async def log_action(
    user_id: str,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None
) -> dict:
    """
    Log a security-relevant action.

    Args:
        user_id: ID of the user performing the action
        action: Action type (e.g., USER_LOGIN, DOCUMENT_UPLOADED)
        resource_type: Type of resource affected (e.g., document, user, workflow)
        resource_id: ID of the affected resource
        details: Additional details about the action
        ip_address: Client IP address

    Returns:
        Created audit log entry
    """
    log_entry = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "details": details or {},
        "ip_address": ip_address,
        "created_at": datetime.utcnow().isoformat()
    }

    # Store log (in production, this would go to database)
    _audit_logs.append(log_entry)

    # Also log to standard logger
    logger.info(
        f"AUDIT: {action} by user {user_id} "
        f"on {resource_type}/{resource_id} - {details}"
    )

    return log_entry


async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 1,
    page_size: int = 50
) -> tuple:
    """
    Retrieve audit logs with filtering.

    Returns:
        Tuple of (logs list, total count)
    """
    filtered_logs = _audit_logs.copy()

    # Apply filters
    if user_id:
        filtered_logs = [l for l in filtered_logs if l["user_id"] == user_id]

    if action:
        filtered_logs = [l for l in filtered_logs if l["action"] == action]

    if resource_type:
        filtered_logs = [l for l in filtered_logs if l["resource_type"] == resource_type]

    if date_from:
        filtered_logs = [l for l in filtered_logs if l["created_at"] >= date_from]

    if date_to:
        filtered_logs = [l for l in filtered_logs if l["created_at"] <= date_to]

    # Sort by date descending
    filtered_logs.sort(key=lambda x: x["created_at"], reverse=True)

    # Paginate
    total = len(filtered_logs)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = filtered_logs[start:end]

    return paginated, total


# Standard action types
class AuditActions:
    # User actions
    USER_REGISTERED = "USER_REGISTERED"
    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    USER_ROLE_UPDATED = "USER_ROLE_UPDATED"
    USER_DELETED = "USER_DELETED"

    # Document actions
    DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED"
    DOCUMENT_VIEWED = "DOCUMENT_VIEWED"
    DOCUMENT_DOWNLOADED = "DOCUMENT_DOWNLOADED"
    DOCUMENT_UPDATED = "DOCUMENT_UPDATED"
    DOCUMENT_DELETED = "DOCUMENT_DELETED"

    # Workflow actions
    WORKFLOW_CREATED = "WORKFLOW_CREATED"
    WORKFLOW_UPDATED = "WORKFLOW_UPDATED"
    WORKFLOW_DELETED = "WORKFLOW_DELETED"
    WORKFLOW_TOGGLED = "WORKFLOW_TOGGLED"
    WORKFLOW_TRIGGERED = "WORKFLOW_TRIGGERED"

    # Security events
    LOGIN_FAILED = "LOGIN_FAILED"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
