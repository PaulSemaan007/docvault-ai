"""
Authentication Service.
Handles user registration and login via Supabase Auth.
"""

from typing import Optional
from datetime import datetime
import uuid
from passlib.context import CryptContext

from app.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory user store for development (replace with Supabase in production)
_users = {}


class AuthService:
    """
    Service for user authentication operations.
    """

    def __init__(self):
        """Initialize with Supabase client (when configured)."""
        # In production, initialize Supabase client here
        pass

    async def register(
        self,
        email: str,
        password: str,
        full_name: str
    ) -> dict:
        """
        Register a new user.

        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            full_name: User's full name

        Returns:
            Created user dict (without password)

        Raises:
            Exception if email already exists
        """
        # Check if email exists
        for user in _users.values():
            if user["email"] == email:
                raise Exception("Email already registered")

        # Create user
        user_id = str(uuid.uuid4())
        hashed_password = pwd_context.hash(password)

        user = {
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "password_hash": hashed_password,
            "role": "user",  # Default role
            "created_at": datetime.utcnow().isoformat()
        }

        _users[user_id] = user

        # Return user without password
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "created_at": user["created_at"]
        }

    async def login(self, email: str, password: str) -> dict:
        """
        Authenticate a user.

        Args:
            email: User's email
            password: Plain text password

        Returns:
            User dict if authenticated

        Raises:
            Exception if credentials invalid
        """
        # Find user by email
        user = None
        for u in _users.values():
            if u["email"] == email:
                user = u
                break

        if not user:
            raise Exception("Invalid credentials")

        # Verify password
        if not pwd_context.verify(password, user["password_hash"]):
            raise Exception("Invalid credentials")

        # Return user without password
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "created_at": user["created_at"]
        }

    async def get_user(self, user_id: str) -> Optional[dict]:
        """
        Get a user by ID.
        """
        user = _users.get(user_id)
        if not user:
            return None

        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "created_at": user["created_at"]
        }

    async def update_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Update a user's password.
        """
        user = _users.get(user_id)
        if not user:
            raise Exception("User not found")

        if not pwd_context.verify(current_password, user["password_hash"]):
            raise Exception("Current password incorrect")

        user["password_hash"] = pwd_context.hash(new_password)
        return True
