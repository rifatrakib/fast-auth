from fastapi import FastAPI

from server.core.config import settings
from server.routers.auth import router as auth_router
from server.routers.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/health")
async def health():
    return settings
