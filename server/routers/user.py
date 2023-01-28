from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}")
async def read_user_by_id(id: int):
    return {"id": id}
