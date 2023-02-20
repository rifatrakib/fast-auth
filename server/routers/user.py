from fastapi import APIRouter

from server.services.validators import Tags

router = APIRouter(prefix="/users", tags=[Tags.users])


@router.get("/{id}")
async def read_user_by_id(id: int):
    return {"id": id}
