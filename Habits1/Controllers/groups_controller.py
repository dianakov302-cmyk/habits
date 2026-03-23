from fastapi import APIRouter, Body
from BusinessLogic.Services.group_service import (
    get_groups,
    create_group,
    join_group
)

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/")
def all_groups():
    return get_groups()


@router.post("/create")
def create(name: str = Body(...)):
    return create_group(name)


@router.post("/join")
def join(group_id: str = Body(...), user_id: str = Body(...)):
    return join_group(group_id, user_id)