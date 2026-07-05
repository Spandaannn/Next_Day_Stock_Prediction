"""
preprocess.py
-------------
Day 1 task (Person 1): Clean raw.csv into a reliable dataset.

Concept notes:
- Missing values: markets are closed on weekends/holidays, so gaps in
  dates are NORMAL and not "missing data" — we only worry about missing
  values WITHIN existing rows (e.g., a NaN Close price).
- Duplicates: sometimes downloads overlap or get re-run; duplicate
  (Date, Ticker) rows would double-count that day everywhere downstream.
- Date conversion: dates often load as strings ("2024-01-05") instead of
  real datetime objects. Without conversion, sorting and rolling
  calculations (Day 2) will behave incorrectly or throw errors.
- Sorting: time-series logic (moving averages, lag features, backtesting)
  assumes row N happened before row N+1. If the data isn't sorted by
  Date within each Ticker, every rolling calculation later will be wrong.
"""

import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/raw.csv")
PROCESSED_DIR = Path("data/processed")


def load_raw_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    initial_rows = len(df)

    # 1. Convert Date column from string to real datetime objects
    df["Date"] = pd.to_datetime(df["Date"])

    # 2. Drop exact duplicate rows (same Date + Ticker + prices)
    df = df.drop_duplicates(subset=["Date", "Ticker"], keep="first")

    # 3. Check and handle missing values in price/volume columns
    price_cols = ["Open", "High", "Low", "Close", "Volume"]
    missing_before = df[price_cols].isna().sum().sum()
    if missing_before > 0:
        print(f"Found {missing_before} missing values — dropping those rows.")
        df = df.dropna(subset=price_cols)
    else:
        print("No missing values found in price/volume columns.")

    # 4. Sort by Ticker then Date — CRITICAL for time-series correctness
    df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)

    # 5. Sanity check: High should never be less than Low, Close, or Open
    bad_rows = df[df["High"] < df[["Open", "Low", "Close"]].max(axis=1)]
    if not bad_rows.empty:
        print(f"WARNING: {len(bad_rows)} rows have inconsistent High/Low/Open/Close values. Inspect manually.")

    final_rows = len(df)
    print(f"Cleaned data: {initial_rows} -> {final_rows} rows "
          f"({initial_rows - final_rows} removed).")

    return df


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = load_raw_data(RAW_PATH)
    cleaned = clean_data(df)

    output_path = PROCESSED_DIR / "clean.csv"
    cleaned.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")
    print(cleaned.groupby("Ticker")["Date"].agg(["min", "max", "count"]))


if __name__ == "__main__":
    main()
