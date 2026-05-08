from collections.abc import Callable

from fastapi import APIRouter, Body, Depends, Query, HTTPException
from Habits1.business_logic.services.interfaces import IUserService
from Habits1.controllers.requests import (
    UserCredentialsRequest,
    UserLogoutRequest,
    UserProfileUpdateRequest,
)
from Habits1.domain.models.user import UserCreate, UserResponse
from Habits1.business_logic.services.user_service import AuthService
from Habits1.repositories.user_repository import UserRepository
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

def create_router(get_service: Callable[[], IUserService]) -> APIRouter:
    router = APIRouter(prefix="/users", tags=["Users"])

    @router.post("/login")
    def login(
        payload: UserCredentialsRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        return service.login_user(payload.email, payload.password)

    @router.post("/logout")
    def logout(
        payload: UserLogoutRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        return service.logout_user(payload.email)

    @router.post("/register")
    def register(
        payload: UserCredentialsRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        return service.register_user(payload.email, payload.password)

    @router.get("/profile")
    def get_profile(
        email: str = Query(...),
        service: IUserService = Depends(get_service),
    ):
        return service.get_user_profile(email)

    @router.put("/profile")
    def update_profile(
        payload: UserProfileUpdateRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        return service.update_user_profile(
            payload.email,
            payload.new_email,
            payload.new_password,
        )

    return router

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

# Ініціалізація (можна винести в dependencies пізніше)
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME", "habitdb")]

user_repo = UserRepository(db)
auth_service = AuthService(user_repo)

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    try:
        return await auth_service.register(user_data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Помилка сервера")
