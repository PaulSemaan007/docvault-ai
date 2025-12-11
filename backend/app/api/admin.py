"""
Admin API endpoints.
User management and audit log access.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

from app.security.jwt import get_current_user, require_role
from app.security.audit import log_action
from app.services.admin_service import AdminService

router = APIRouter()


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: str
    document_count: int


class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int


class UpdateRoleRequest(BaseModel):
    role: str  # admin, manager, user


class AuditLogEntry(BaseModel):
    id: str
    user_id: str
    user_email: Optional[str]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[str]
    details: Optional[dict]
    ip_address: Optional[str]
    created_at: str


class AuditLogResponse(BaseModel):
    logs: List[AuditLogEntry]
    total: int
    page: int
    page_size: int


class DashboardStats(BaseModel):
    total_users: int
    total_documents: int
    documents_today: int
    documents_this_week: int
    classification_breakdown: dict
    storage_used_mb: float


@router.get("/users", response_model=UserListResponse)
async def list_users(
    role: Optional[str] = None,
    current_user: dict = Depends(require_role(["admin"]))
):
    """
    List all users (admin only).
    """
    admin_service = AdminService()

    users = await admin_service.list_users(role=role)

    return UserListResponse(
        users=[UserResponse(**u) for u in users],
        total=len(users)
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: dict = Depends(require_role(["admin"]))
):
    """
    Get a specific user by ID (admin only).
    """
    admin_service = AdminService()

    user = await admin_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(**user)


@router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: str,
    request: UpdateRoleRequest,
    current_user: dict = Depends(require_role(["admin"]))
):
    """
    Update a user's role (admin only).

    Available roles:
    - admin: Full access to all features
    - manager: Can create workflows, view all documents
    - user: Can only manage own documents
    """
    if request.role not in ["admin", "manager", "user"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role. Must be one of: admin, manager, user"
        )

    # Prevent self-demotion
    if user_id == current_user["id"] and request.role != "admin":
        raise HTTPException(
            status_code=400,
            detail="Cannot change your own admin role"
        )

    admin_service = AdminService()

    user = await admin_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = await admin_service.update_role(user_id, request.role)

    await log_action(
        user_id=current_user["id"],
        action="USER_ROLE_UPDATED",
        resource_type="user",
        resource_id=user_id,
        details={"old_role": user["role"], "new_role": request.role}
    )

    return UserResponse(**updated)


@router.get("/audit-logs", response_model=AuditLogResponse)
async def get_audit_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 1,
    page_size: int = 50,
    current_user: dict = Depends(require_role(["admin"]))
):
    """
    View audit logs with filtering (admin only).

    Logs all security-relevant actions:
    - User registration, login, logout
    - Document uploads, downloads, deletions
    - Workflow creation, modification, deletion
    - Role changes
    """
    admin_service = AdminService()

    logs, total = await admin_service.get_audit_logs(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size
    )

    return AuditLogResponse(
        logs=[AuditLogEntry(**log) for log in logs],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: dict = Depends(require_role(["admin", "manager"]))
):
    """
    Get dashboard statistics (admin and manager).
    """
    admin_service = AdminService()

    stats = await admin_service.get_dashboard_stats()

    return DashboardStats(**stats)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_role(["admin"]))
):
    """
    Delete a user and all their documents (admin only).
    """
    if user_id == current_user["id"]:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )

    admin_service = AdminService()

    user = await admin_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await admin_service.delete_user(user_id)

    await log_action(
        user_id=current_user["id"],
        action="USER_DELETED",
        resource_type="user",
        resource_id=user_id,
        details={"email": user["email"]}
    )

    return {"message": "User deleted successfully"}
