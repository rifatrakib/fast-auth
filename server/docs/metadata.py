from server.core.config import settings
from server.services.validators import Tags


def read_api_metadata():
    with open("server/docs/README.md") as reader:
        description = reader.read()

    return {
        "title": settings.APP_NAME,
        "description": description,
        "version": "0.0.1",
        "terms_of_service": "https://fastapi.tiangolo.com/",
        "contact": {
            "name": f"Maintainer: {settings.APP_NAME}",
            "url": "https://fastapi.tiangolo.com/",
            "email": "Rakib.1508@outlook.com",
        },
    }


def read_tags_metadata():
    return [
        {
            "name": Tags.server_health.value,
            "description": "Verify *server operability* and *configuration variables*.",
            "externalDocs": {
                "description": "Server Health Check",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
        {
            "name": Tags.authentication.value,
            "description": "Endpoints for *user authentication*",
            "externalDocs": {
                "description": "User authentication documentation",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
        {
            "name": Tags.users.value,
            "description": "Endpoints for *user information*",
            "externalDocs": {
                "description": "Users information documentation",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
    ]
