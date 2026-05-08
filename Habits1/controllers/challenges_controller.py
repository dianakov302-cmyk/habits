from collections.abc import Callable

from fastapi import APIRouter, Depends
from Habits1.business_logic.services.interfaces import IChallengeService
from Habits1.controllers.requests import ChallengeCreateRequest

def create_router(get_service: Callable[[], IChallengeService]) -> APIRouter:
    router = APIRouter(prefix="/challenges", tags=["Challenges"])

    @router.get("/")
    def all_challenges(service: IChallengeService = Depends(get_service)):
        return service.get_challenges()

    @router.post("/create")
    def create(
        payload: ChallengeCreateRequest,
        service: IChallengeService = Depends(get_service),
    ):
        return service.create_challenge(payload.title)

    return router
