"""
train.py
--------
Trains the stock direction prediction models.

Owner: Person 1 (ML Engineer) — this file is scaffolded on Day 1
so the project structure is in place; Person 1 fills in the logic
on Day 3.

Expected flow:
    1. Load processed dataset from data/processed/processed.csv
    2. Time-based train/test split (NO shuffling — prevents leakage)
    3. Train Logistic Regression (baseline)
    4. Train Random Forest (main model)
    5. Save best model to models/model.pkl (use joblib)

Run:
    python src/train.py
"""

import pandas as pd
import joblib
from pathlib import Path

PROCESSED_DATA_PATH = Path("data/processed/processed.csv")
MODEL_OUTPUT_PATH = Path("models/model.pkl")


def load_data(path: Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    """Load the feature-engineered dataset."""
    # TODO (Person 1): implement once features.py produces processed.csv
    raise NotImplementedError("load_data: waiting on Day 2 feature engineering output")


def time_based_split(df: pd.DataFrame, test_size: float = 0.2):
    """Split chronologically — train on earlier dates, test on later dates."""
    # TODO (Person 1): implement time-based split (no random shuffling!)
    raise NotImplementedError("time_based_split: to be implemented on Day 3")


def train_models(X_train, y_train):
    """Train Logistic Regression (baseline) and Random Forest (main)."""
    # TODO (Person 1): fit LogisticRegression and RandomForestClassifier
    raise NotImplementedError("train_models: to be implemented on Day 3")


def save_model(model, path: Path = MODEL_OUTPUT_PATH):
    """Persist the trained model with joblib."""
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    print(f"Model saved to {path}")


if __name__ == "__main__":
    df = load_data()
    # X_train, X_test, y_train, y_test = time_based_split(df)
    # model = train_models(X_train, y_train)
    # save_model(model)
    print("train.py scaffold ready — implement steps above on Day 3.")
