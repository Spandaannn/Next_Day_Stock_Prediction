"""
evaluate.py
-----------
Computes evaluation metrics for the trained model(s): Accuracy, Precision,
Recall, F1, Confusion Matrix, and Feature Importance.

Owner: Person 1 (ML Engineer) — implemented on Day 3, alongside train.py.

Run:
    python src/evaluate.py
"""

import pandas as pd
from pathlib import Path
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

REPORTS_DIR = Path("outputs/reports")


def evaluate_model(model, X_test, y_test) -> dict:
    """Compute standard classification metrics."""
    # TODO (Person 1): implement on Day 3
    y_pred = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }


def feature_importance(model, feature_names):
    """Extract and rank feature importances (Random Forest)."""
    # TODO (Person 1): implement on Day 3
    raise NotImplementedError("feature_importance: to be implemented on Day 3")


def save_report(metrics: dict, filename: str = "evaluation_report.txt"):
    """Write metrics to outputs/reports/."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / filename
    with open(path, "w") as f:
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    print(f"Report saved to {path}")


if __name__ == "__main__":
    print("evaluate.py scaffold ready — implement steps above on Day 3.")
