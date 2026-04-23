"""Train and compare ML classifiers for Falcon 9 first-stage landing prediction."""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from project_paths import ASSETS_DIR, ensure_directories, find_data_file

MODEL_SCORES_CSV = ASSETS_DIR / "model_scores.csv"
CONFUSION_MATRIX_PNG = ASSETS_DIR / "confusion_matrix.png"


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    return pd.read_csv(find_data_file("dataset_part_2.csv")), pd.read_csv(find_data_file("dataset_part_3.csv"))


def save_confusion_matrix(y_true, y_pred) -> None:
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    fig.savefig(CONFUSION_MATRIX_PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_directories()
    data, X = load_inputs()
    y = data["Class"].to_numpy()
    X = X.fillna(0)
    X_scaled = preprocessing.StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=2)

    models = {
        "Logistic Regression": GridSearchCV(LogisticRegression(max_iter=1000), {"C": [0.1, 1.0], "solver": ["lbfgs"]}, cv=5, n_jobs=1),
        "SVM": GridSearchCV(SVC(), {"kernel": ["linear", "sigmoid"], "C": [0.1, 1.0], "gamma": ["scale", "auto"]}, cv=5, n_jobs=1),
        "Decision Tree": GridSearchCV(DecisionTreeClassifier(random_state=2), {"criterion": ["gini", "entropy"], "max_depth": [2, 4, 6]}, cv=5, n_jobs=1),
        "KNN": GridSearchCV(KNeighborsClassifier(), {"n_neighbors": [3, 5, 7], "p": [1, 2]}, cv=5, n_jobs=1),
    }

    records: list[dict[str, object]] = []
    best_name = ""
    best_model = None
    best_score = -1.0

    for name, model in models.items():
        model.fit(X_train, y_train)
        score = float(model.score(X_test, y_test))
        records.append({"model": name, "test_accuracy": score, "best_params": str(model.best_params_)})
        print(f"{name}: {score:.4f} | {model.best_params_}")
        if score > best_score:
            best_name = name
            best_model = model
            best_score = score

    pd.DataFrame(records).sort_values("test_accuracy", ascending=False).to_csv(MODEL_SCORES_CSV, index=False)
    if best_model is not None:
        save_confusion_matrix(y_test, best_model.predict(X_test))
    print(f"Best model: {best_name} ({best_score:.4f})")
    print(f"Saved {MODEL_SCORES_CSV}")
    print(f"Saved {CONFUSION_MATRIX_PNG}")


if __name__ == "__main__":
    main()
