from fastapi.testclient import TestClient
from service.app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict():
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    body = r.json()
    assert body["predicted_class"] in [0, 1, 2]
    assert body["class_name"] in ["setosa", "versicolor", "virginica"]
