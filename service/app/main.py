from __future__ import annotations

import os
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

MODEL_PATH = os.getenv("MODEL_PATH", "artifacts/iris_model.joblib")

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
target_names = bundle["target_names"]

app = FastAPI(title="Iris ML API", version="1.0.0")


class PredictRequest(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        examples=[[5.1, 3.5, 1.4, 0.2]],
    )


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs", status_code=307)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    if len(req.features) != 4:
        raise HTTPException(status_code=400, detail="features must have exactly 4 values")

    x = np.array([req.features], dtype=float)
    proba = model.predict_proba(x)[0]
    idx = int(np.argmax(proba))

    return {
        "input": req.features,
        "prediction": {
            "class_index": idx,
            "class_name": target_names[idx],
            "probabilities": proba.tolist(),
        },
    }
