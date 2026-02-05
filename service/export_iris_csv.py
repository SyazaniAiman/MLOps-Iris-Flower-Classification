import csv
import os
from sklearn.datasets import load_iris

OUT_PATH = os.path.join("data", "iris.csv")

def main():
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names

    os.makedirs("data", exist_ok=True)

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(feature_names + ["target", "class_name"])

        for i in range(len(X)):
            class_name = target_names[int(y[i])]
            writer.writerow(list(X[i]) + [int(y[i]), class_name])

    print(f"Saved: {OUT_PATH}")
    print(f"Rows: {len(X)}, Columns: {len(feature_names) + 2}")

if __name__ == "__main__":
    main()
