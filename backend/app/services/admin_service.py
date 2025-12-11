"""
Admin Service.
User management and system administration operations.
"""

from typing import Optional, List, Tuple
from datetime import datetime, timedelta

from app.services.auth_service import _users
from app.services.document_service import _documents
from app.security.audit import _audit_logs


class AdminService:
    """
    Service for admin operations.
    """

    async def list_users(self, role: Optional[str] = None) -> List[dict]:
        """
        List all users with optional role filter.
        """
        users = []

        for user in _users.values():
            if role and user["role"] != role:
                continue

            # Count user's documents
            doc_count = len([
                d for d in _documents.values()
                if d["user_id"] == user["id"]
            ])

            users.append({
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "created_at": user["created_at"],
                "document_count": doc_count
            })

        users.sort(key=lambda x: x["created_at"], reverse=True)
        return users

    async def get_user(self, user_id: str) -> Optional[dict]:
        """Get a specific user by ID."""
        user = _users.get(user_id)
        if not user:
            return None

        doc_count = len([
            d for d in _documents.values()
            if d["user_id"] == user_id
        ])

        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "created_at": user["created_at"],
            "document_count": doc_count
        }

    async def update_role(self, user_id: str, new_role: str) -> dict:
        """Update a user's role."""
        user = _users.get(user_id)
        if not user:
            raise Exception("User not found")

        user["role"] = new_role

        doc_count = len([
            d for d in _documents.values()
            if d["user_id"] == user_id
        ])

        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "created_at": user["created_at"],
            "document_count": doc_count
        }

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user and their documents."""
        if user_id not in _users:
            return False

        # Delete user's documents
        docs_to_delete = [
            d["id"] for d in _documents.values()
            if d["user_id"] == user_id
        ]
        for doc_id in docs_to_delete:
            del _documents[doc_id]

        # Delete user
        del _users[user_id]
        return True

    async def get_audit_logs(
        self,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[dict], int]:
        """Get audit logs with filtering."""
        logs = _audit_logs.copy()

        # Apply filters
        if user_id:
            logs = [l for l in logs if l["user_id"] == user_id]
        if action:
            logs = [l for l in logs if l["action"] == action]
        if resource_type:
            logs = [l for l in logs if l["resource_type"] == resource_type]
        if date_from:
            logs = [l for l in logs if l["created_at"] >= date_from]
        if date_to:
            logs = [l for l in logs if l["created_at"] <= date_to]

        # Add user email to logs
        for log in logs:
            user = _users.get(log["user_id"])
            log["user_email"] = user["email"] if user else None

        # Sort and paginate
        logs.sort(key=lambda x: x["created_at"], reverse=True)

        total = len(logs)
        start = (page - 1) * page_size
        end = start + page_size

        return logs[start:end], total

    async def get_dashboard_stats(self) -> dict:
        """Get dashboard statistics."""
        now = datetime.utcnow()
        today = now.date().isoformat()
        week_ago = (now - timedelta(days=7)).isoformat()

        total_users = len(_users)
        total_documents = len(_documents)

        # Documents today
        docs_today = len([
            d for d in _documents.values()
            if d["created_at"].startswith(today)
        ])

        # Documents this week
        docs_this_week = len([
            d for d in _documents.values()
            if d["created_at"] >= week_ago
        ])

        # Classification breakdown
        classification_breakdown = {}
        for doc in _documents.values():
            cls = doc.get("classification") or "unclassified"
            classification_breakdown[cls] = classification_breakdown.get(cls, 0) + 1

        # Storage used (approximate)
        storage_bytes = sum(d.get("file_size", 0) for d in _documents.values())
        storage_mb = storage_bytes / (1024 * 1024)

        return {
            "total_users": total_users,
            "total_documents": total_documents,
            "documents_today": docs_today,
            "documents_this_week": docs_this_week,
            "classification_breakdown": classification_breakdown,
            "storage_used_mb": round(storage_mb, 2)
        }
