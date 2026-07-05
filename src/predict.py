"""
predict.py
----------
Loads the trained model and outputs an UP / DOWN prediction for the
latest available stock data.

Owner: Person 2 (Software Engineer) — implemented on Day 3.

Expected flow:
    1. Load model.pkl from models/
    2. Load latest row(s) of feature data (same feature pipeline as training)
    3. Run model.predict() / predict_proba()
    4. Print/return "UP" or "DOWN" (and optionally the confidence)

Run:
    python src/predict.py --ticker TCS.NS
"""

import argparse
import joblib
from pathlib import Path

MODEL_PATH = Path("models/model.pkl")


def load_model(path: Path = MODEL_PATH):
    """Load the trained model artifact."""
    if not path.exists():
        raise FileNotFoundError(
            f"No model found at {path}. Run src/train.py first (Day 3)."
        )
    return joblib.load(path)


def get_latest_features(ticker: str):
    """
    Fetch/compute the latest feature row for `ticker`.

    Must reuse the exact same feature engineering logic as features.py
    to avoid train/serve skew.
    """
    # TODO (Person 2, with Person 1's features.py as reference): implement Day 3
    raise NotImplementedError("get_latest_features: to be implemented on Day 3")


def predict_direction(ticker: str) -> str:
    """Return 'UP' or 'DOWN' for the given ticker."""
    model = load_model()
    features = get_latest_features(ticker)
    prediction = model.predict(features)[0]
    return "UP" if prediction == 1 else "DOWN"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict next-day stock direction.")
    parser.add_argument("--ticker", type=str, default="TCS.NS", help="Stock ticker symbol")
    args = parser.parse_args()

    print("predict.py scaffold ready — implement steps above on Day 3.")
    # result = predict_direction(args.ticker)
    # print(f"{args.ticker}: {result}")
