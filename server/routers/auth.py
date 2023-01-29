from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/signup")
async def register_user():
    return {"message": "trial"}
