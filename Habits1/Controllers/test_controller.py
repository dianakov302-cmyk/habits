from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/test")
def test():
    return {"status": "API working"}