from collections.abc import Callable

from fastapi import APIRouter, Depends
from Habits1.business_logic.services.interfaces import IProgressService
from Habits1.controllers.requests import HabitCompletionRequest


def create_router(get_service: Callable[[], IProgressService]) -> APIRouter:
    router = APIRouter(prefix="/progress", tags=["Progress"])

    @router.post("/complete")
    def complete(
        payload: HabitCompletionRequest,
        service: IProgressService = Depends(get_service),
    ):
        return service.complete_habit(payload.user_id, payload.habit_id)

    @router.get("/{user_id}")
    def progress(
        user_id: str,
        service: IProgressService = Depends(get_service),
    ):
        return service.get_user_progress(user_id)

    return router
