from collections.abc import Callable

from fastapi import APIRouter, Depends, HTTPException
from Habits1.business_logic.services.interfaces import IHabitService
from Habits1.controllers.requests import HabitCreateRequest


def create_router(get_service: Callable[[], IHabitService]) -> APIRouter:
    router = APIRouter(prefix="/habits", tags=["Habits"])

    @router.get("/")
    def all_habits(service: IHabitService = Depends(get_service)):
        return service.get_all_habits()

    @router.get("/{habit_id}")
    def habit(habit_id: str, service: IHabitService = Depends(get_service)):
        result = service.get_habit(habit_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Habit not found")
        return result

    @router.post("/create")
    def create(
        payload: HabitCreateRequest,
        service: IHabitService = Depends(get_service),
    ):
        return service.create_habit(payload.name, payload.description)

    @router.delete("/{habit_id}")
    def delete(habit_id: str, service: IHabitService = Depends(get_service)):
        deleted = service.delete_habit(habit_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Habit not found")
        return {"message": "Habit deleted"}


    @router.post("/{habit_id}/complete")
    def mark_habit_as_done(habit_id: str, service: IHabitService = Depends(get_habit_service)):
        return {"new_streak": service.complete_habit(habit_id)}

    return router