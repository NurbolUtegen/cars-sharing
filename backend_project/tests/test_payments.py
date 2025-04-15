from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_payment_success():
    response = client.post("/pay", json={"user_id": 1, "amount": 10.0})
    assert response.status_code == 200
    assert response.json()["status"] == "success"