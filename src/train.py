"""
train.py
--------
Day 3 task (Person 1): Train Logistic Regression (baseline) and
Random Forest (main model) on Target_Direction, using a strict
time-based train/test split.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from features import FEATURE_COLUMNS, scale_features

FEATURES_PATH = Path("data/processed/features.csv")
MODEL_DIR = Path("models")
TEST_FRACTION = 0.2  # last 20% of dates -> test set


def load_features(path: Path = FEATURES_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Date"])
    return df


def time_based_split(df: pd.DataFrame, test_fraction: float = TEST_FRACTION):
    """
    Split by a DATE cutoff (not row index), applied globally across all
    tickers at once. This keeps every ticker's split chronological:
    train = earlier dates, test = later dates, no shuffling.
    """
    unique_dates = np.sort(df["Date"].unique())
    cutoff_idx = int(len(unique_dates) * (1 - test_fraction))
    cutoff_date = unique_dates[cutoff_idx]

    train_df = df[df["Date"] < cutoff_date].reset_index(drop=True)
    test_df = df[df["Date"] >= cutoff_date].reset_index(drop=True)
    return train_df, test_df, cutoff_date


def main():
    df = load_features()
    print(f"Loaded {len(df)} rows, {df['Ticker'].nunique()} tickers")

    train_df, test_df, cutoff_date = time_based_split(df)
    print(f"Split at {cutoff_date} -> train: {len(train_df)} rows, test: {len(test_df)} rows")

    # Scale AFTER splitting - fit only on train (see features.py docstring)
    train_scaled, test_scaled, scaler = scale_features(train_df, test_df)

    X_train, y_train = train_scaled[FEATURE_COLUMNS], train_scaled["Target_Direction"]
    X_test, y_test = test_scaled[FEATURE_COLUMNS], test_scaled["Target_Direction"]

    # --- Baseline: Logistic Regression ---
    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(X_train, y_train)
    log_reg_acc = log_reg.score(X_test, y_test)
    print(f"Logistic Regression test accuracy: {log_reg_acc:.4f}")

    # --- Main model: Random Forest ---
    rf = RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    rf_acc = rf.score(X_test, y_test)
    print(f"Random Forest test accuracy: {rf_acc:.4f}")

    # --- Save the better-performing model, plus the scaler it depends on ---
    # predict.py MUST use this same scaler at inference time - applying the
    # model to unscaled raw features would silently produce garbage predictions.
    if rf_acc >= log_reg_acc:
        best_model, best_name = rf, "RandomForest"
    else:
        best_model, best_name = log_reg, "LogisticRegression"

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_DIR / "model.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
    joblib.dump(FEATURE_COLUMNS, MODEL_DIR / "feature_columns.pkl")
    print(f"\nSaved best model ({best_name}) to {MODEL_DIR / 'model.pkl'}")
    print(f"Saved matching scaler to {MODEL_DIR / 'scaler.pkl'}")


if __name__ == "__main__":
    main()
