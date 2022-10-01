from fastapi import FastAPI

from . import config

app = FastAPI()


@app.get("/")
def index_page():
    app_name = config.read_config("app_name")
    return {"app_name": app_name}
