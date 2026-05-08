from fastapi import APIRouter, Depends
from business_logic.services.punchcard_service import PunchCardService

router = APIRouter(prefix="/loyalty")

@router.post("/punch/{user_id}")
async def punch(user_id: str, service: LoyaltyService = Depends()):
    return await service.add_punch_to_user(user_id)