import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def main():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=500))
    ])
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(model, "artifacts/iris_model.joblib")

    with open("artifacts/metrics.txt", "w", encoding="utf-8") as f:
        f.write(f"accuracy={acc:.4f}\n")

    print(f"Saved artifacts/iris_model.joblib | accuracy={acc:.4f}")

if __name__ == "__main__":
    main()
