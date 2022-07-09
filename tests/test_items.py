from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_read_item_by_id():
    response = client.get("/items/1?include_name=true")

    assert response.status_code == 200
    assert response.json() == {
        "item_id": 1,
        "include_name": True,
        "include_create_date": True,
        "include_location": None,
        "query": None  
    }