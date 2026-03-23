from fastapi import APIRouter, Body
from BusinessLogic.Services.progress_service import (
    complete_habit,
    get_user_progress
)

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.post("/complete")
def complete(
    user_id: str = Body(...),
    habit_id: str = Body(...)
):
    return complete_habit(user_id, habit_id)


@router.get("/{user_id}")
def progress(user_id: str):
    return get_user_progress(user_id)