from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def main():
    root = Path(__file__).resolve().parents[1]   # repo root
    artifacts_dir = root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )

    clf = LogisticRegression(max_iter=500)
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)
    acc = float(accuracy_score(y_test, y_pred))

    payload = {
        "model": clf,
        "target_names": list(iris.target_names),
        "feature_names": list(iris.feature_names),
    }

    joblib.dump(payload, artifacts_dir / "iris_model.joblib")

    with open(artifacts_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump({"accuracy": acc}, f, indent=2)

    print(f"Saved model to {artifacts_dir / 'iris_model.joblib'}")
    print(f"Accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()

