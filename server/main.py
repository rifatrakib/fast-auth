from fastapi import FastAPI

from . import config
from .auth import routes as auth_routes

app = FastAPI()
app.include_router(auth_routes.router)


@app.get("/")
def index_page():
    app_name = config.read_config("app_name")
    return {"app_name": app_name}
