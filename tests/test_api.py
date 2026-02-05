import os
from fastapi.testclient import TestClient

# Make sure this matches your module structure
# If main.py is in service/app/main.py, python path will be set in Jenkins stage
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict():
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "class_name" in data["prediction"]
