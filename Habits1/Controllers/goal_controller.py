from collections.abc import Callable

from fastapi import APIRouter, Body, Depends, Query

from Habits1.business_logic.services.interfaces import IGoalService
from Habits1.controllers.requests import GoalCreateRequest


def create_router(get_service: Callable[[], IGoalService]) -> APIRouter:
    router = APIRouter(prefix="/goals", tags=["Goals"])

    @router.get("/options")
    def options(service: IGoalService = Depends(get_service)):
        return service.get_goal_options()

    @router.post("/set")
    def set_goal(
        payload: GoalCreateRequest = Body(...),
        service: IGoalService = Depends(get_service),
    ):
        return service.set_goal(payload.email, payload.goal_code)

    @router.get("/user")
    def user_goal(
        email: str = Query(...),
        service: IGoalService = Depends(get_service),
    ):
        return service.get_user_goal(email)

    return router
def create_goal_router(get_service: Callable[[], IGoalService]) -> APIRouter:
    return create_router(get_service)

