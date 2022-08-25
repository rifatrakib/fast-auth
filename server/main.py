from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index_page():
    return {"title": "index"}
