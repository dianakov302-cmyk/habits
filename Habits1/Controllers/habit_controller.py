from fastapi import APIRouter, Body
from habit.habit_service import (
    get_all_habits,
    get_habit,
    delete_habit
)

router = APIRouter(prefix="/habits", tags=["Habits"])


@router.get("/")
def all_habits():
    return get_all_habits()


@router.get("/{habit_id}")
def habit(habit_id: str):
    return get_habit(habit_id)


@router.post("/create")
def create(
    name: str = Body(...),
    description: str = Body(...)
):
    return create_habit(name, description)


@router.delete("/{habit_id}")
def delete(habit_id: str):
    return delete_habit(habit_id)