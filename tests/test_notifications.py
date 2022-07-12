from fastapi.testclient import TestClient
from src.main import app
from src.dependencies.dependencies import get_query

client = TestClient(app)

def mock_get_query():
    return {}

app.dependency_overrides[get_query] = mock_get_query


def test_send_notifications(mocker):
    mock_write_logs = mocker.patch("src.routers.notifications.write_log")

    email = 'test@test.com'
    response = client.post(f"/notifications/send-notification/{email}?q=testing")

    assert response.status_code == 200
    assert response.json() ==  {"message": "Message sent"}
    assert mock_write_logs.call_count == 1