from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_send_notifications():
    email = 'test@test.com'
    response = client.post(f"/notifications/send-notification/{email}")

    assert response.status_code == 200
    assert response.json() ==  {"message": "Message sent"}