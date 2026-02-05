from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import joblib
import numpy as np
import os

APP_TITLE = "Iris Model API"
MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/model.joblib")

app = FastAPI(title=APP_TITLE)

class PredictRequest(BaseModel):
    # Iris features in the canonical order:
    # sepal length, sepal width, petal length, petal width
    features: List[List[float]] = Field(
        ...,
        examples=[[[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]]
    )

class PredictResponse(BaseModel):
    predictions: List[int]
    probabilities: List[List[float]]

model = None

@app.on_event("startup")
def load_model():
    global model
    model = joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    ok = model is not None
    return {"status": "ok" if ok else "not_ready", "model_path": MODEL_PATH}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    X = np.array(req.features, dtype=float)
    preds = model.predict(X).tolist()

    # If classifier supports predict_proba
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X).tolist()
    else:
        probs = [[None] for _ in preds]

    return {"predictions": preds, "probabilities": probs}
