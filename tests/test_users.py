from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_user_by_id():
    headers = { "x-token": "fake-super-secret-token", "x-key": "fake-super-secret-key" }
    response = client.get("/users/1", headers=headers)

    assert response.status_code == 200
    assert response.json() == { "user_id": "1" }