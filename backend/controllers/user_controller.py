from collections.abc import Callable

from fastapi import APIRouter, Body, Depends, Query

from backend.business_logic.services.interfaces import IUserService
from backend.controllers.requests import (
    UserCredentialsRequest,
    UserLogoutRequest,
    UserProfileUpdateRequest,
    UserQuizResultRequest,
)


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
        return service.register_user(payload.email, payload.password, payload.name)

    @router.post("/test-result")
    def save_test_result(
        payload: UserQuizResultRequest = Body(...),
        service: IUserService = Depends(get_service),
    ):
        return service.save_test_result(
            payload.session_id,
            payload.answers,
            payload.profile,
            payload.roadmap,
            payload.email,
        )

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
