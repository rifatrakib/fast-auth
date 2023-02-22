from fastapi import FastAPI

from server.core.config import settings
from server.docs.metadata import read_api_metadata, read_tags_metadata
from server.routers.auth import router as auth_router
from server.routers.user import router as user_router

app = FastAPI(
    **read_api_metadata(),
    openapi_tags=read_tags_metadata(),
)

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/health")
async def health():
    return settings
