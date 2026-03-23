from fastapi import APIRouter, Body
from BusinessLogic.Services.challenge_service import (
    get_challenges,
    create_challenge
)

router = APIRouter(prefix="/challenges", tags=["Challenges"])


@router.get("/")
def all_challenges():
    return get_challenges()


@router.post("/create")
def create(title: str = Body(...)):
    return create_challenge(title)