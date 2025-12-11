"""
Authentication API endpoints.
Handles user registration, login, and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.security.jwt import create_access_token, get_current_user
from app.security.audit import log_action
from app.services.auth_service import AuthService

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: str


@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest):
    """
    Register a new user account.

    - Creates user in Supabase Auth
    - Creates user profile with default 'user' role
    - Returns JWT token for immediate login
    """
    auth_service = AuthService()

    try:
        user = await auth_service.register(
            email=request.email,
            password=request.password,
            full_name=request.full_name
        )

        token = create_access_token({"sub": user["id"], "role": user["role"]})

        await log_action(
            user_id=user["id"],
            action="USER_REGISTERED",
            resource_type="user",
            resource_id=user["id"]
        )

        return TokenResponse(
            access_token=token,
            user=user
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and return JWT token.
    """
    auth_service = AuthService()

    try:
        user = await auth_service.login(
            email=request.email,
            password=request.password
        )

        token = create_access_token({"sub": user["id"], "role": user["role"]})

        await log_action(
            user_id=user["id"],
            action="USER_LOGIN",
            resource_type="user",
            resource_id=user["id"]
        )

        return TokenResponse(
            access_token=token,
            user=user
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    """
    return UserResponse(**current_user)


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Log out the current user.
    Note: JWT is stateless, so this mainly logs the action.
    """
    await log_action(
        user_id=current_user["id"],
        action="USER_LOGOUT",
        resource_type="user",
        resource_id=current_user["id"]
    )

    return {"message": "Successfully logged out"}
