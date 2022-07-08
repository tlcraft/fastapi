from fastapi.testclient import TestClient
from src.enums.model_name import ModelName
from src.main import app

client = TestClient(app)


def test_read_models_by_name_with_alexnet():
    test_model_name = ModelName.alexnet
    response = client.get(f"/models/{test_model_name}")
    assert response.status_code == 200
    assert response.json() == {"model_name": test_model_name, "message": "Deep Learning FTW!"}