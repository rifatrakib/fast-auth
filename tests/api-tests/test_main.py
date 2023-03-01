from fastapi.testclient import TestClient

from server.core.config import settings
from server.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    response.status_code == 200
    response_body = response.json()
    assert response_body["appName"] == settings.APP_NAME
    assert response_body["mode"] == settings.MODE
    assert response_body["debug"] == settings.DEBUG
