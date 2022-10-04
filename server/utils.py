import os


def get_url():
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    server = os.environ.get("DB_HOST") + ":" + os.environ.get("DB_PORT")
    db = os.environ.get("DATABASE_NAME")
    return f"postgresql://{user}:{password}@{server}/{db}"
