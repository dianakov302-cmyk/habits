from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import Optional
from BusinessLogic.Services.user_service import login_user
from BusinessLogic.Services.user_service import logout_user
from BusinessLogic.Services.user_service import register_user
from BusinessLogic.Services.user_service import get_user_profile
from BusinessLogic.Services.user_service import update_user_profile
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
def login(email: str, password: str):
    result = login_user(email, password)
    return result

@router.post("/logout")
def logout(email: str):
    # Implement logout logic if needed (e.g., token invalidation)
    return {"status": "success", "message": "Logout successful. See you next time!"}


@router.post("/register")
def register(email: str, password: str):
    result = register_user(email, password)
    return result


@router.get("/profile")
def get_profile(email: str):
    result = get_user_profile(email)
    return result


@router.put("/profile")
def update_profile(email: str, new_email: str = None, new_password: str = None):
    result = update_user_profile(email, new_email, new_password)
    return result