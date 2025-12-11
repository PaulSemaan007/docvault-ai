"""
JWT Authentication and Authorization.
Handles token creation, validation, and role-based access control.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Callable
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings

# HTTP Bearer scheme for token extraction
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.

    Args:
        data: Payload data (should include 'sub' for user ID)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiration_minutes)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT string to decode

    Returns:
        Decoded payload dict

    Raises:
        HTTPException if token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    FastAPI dependency to get the current authenticated user.

    Usage:
        @router.get("/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            ...
    """
    token = credentials.credentials
    payload = decode_token(token)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # In production, fetch user from database here
    # For now, return payload data
    return {
        "id": user_id,
        "role": payload.get("role", "user"),
        "email": payload.get("email", ""),
        "full_name": payload.get("full_name", "")
    }


def require_role(allowed_roles: List[str]) -> Callable:
    """
    Create a dependency that requires specific roles.

    Usage:
        @router.post("/admin-only")
        async def admin_route(current_user: dict = Depends(require_role(["admin"]))):
            ...
    """
    async def role_checker(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> dict:
        token = credentials.credentials
        payload = decode_token(token)

        user_id = payload.get("sub")
        user_role = payload.get("role", "user")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )

        return {
            "id": user_id,
            "role": user_role,
            "email": payload.get("email", ""),
            "full_name": payload.get("full_name", "")
        }

    return role_checker


def create_refresh_token(user_id: str) -> str:
    """
    Create a refresh token with longer expiration.
    """
    return create_access_token(
        {"sub": user_id, "type": "refresh"},
        expires_delta=timedelta(days=7)
    )


def verify_refresh_token(token: str) -> str:
    """
    Verify a refresh token and return the user ID.
    """
    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    return payload.get("sub")
