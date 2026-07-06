"""
features.py
------------
Day 2 task (Person 1): Feature engineering + target label creation.

CRITICAL RULE: every rolling/shift calculation below is done per-ticker
(groupby("Ticker")), never across the whole dataframe. Mixing tickers in
a rolling window would leak one stock's prices into another's indicators.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler

INPUT_PATH = Path("data/processed/clean.csv")
OUTPUT_PATH = Path("data/processed/features.csv")


def load_data(path: Path = INPUT_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Date"])
    df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """All feature engineering happens here, step by step."""
    df = df.copy()
    grp = df.groupby("Ticker", group_keys=False)

    # --- Daily Return: simple % change in Close vs. previous day ---
    df["Daily_Return"] = grp["Close"].pct_change()

    # --- 20-day EMA: exponential moving average, reacts faster than a simple MA ---
    df["EMA_20"] = grp["Close"].transform(lambda s: s.ewm(span=20, adjust=False).mean())

    # --- Volume Momentum: today's volume relative to its own 10-day average ---
    df["Volume_MA_10"] = grp["Volume"].transform(lambda s: s.rolling(window=10).mean())
    df["Volume_Momentum"] = df["Volume"] / df["Volume_MA_10"]

    # --- RSI (14-day): ratio of average gains to average losses ---
    def rsi(series: pd.Series, window: int = 14) -> pd.Series:
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    df["RSI_14"] = grp["Close"].transform(rsi)

    # --- MACD: fast EMA (12) minus slow EMA (26), plus a 9-day signal line ---
    ema_12 = grp["Close"].transform(lambda s: s.ewm(span=12, adjust=False).mean())
    ema_26 = grp["Close"].transform(lambda s: s.ewm(span=26, adjust=False).mean())
    df["MACD_Line"] = ema_12 - ema_26
    df["MACD_Signal"] = df.groupby("Ticker")["MACD_Line"].transform(
        lambda s: s.ewm(span=9, adjust=False).mean()
    )
    df["MACD_Histogram"] = df["MACD_Line"] - df["MACD_Signal"]

    # --- Bollinger Bands: 20-day SMA +/- 2 standard deviations ---
    bb_mid = grp["Close"].transform(lambda s: s.rolling(window=20).mean())
    bb_std = grp["Close"].transform(lambda s: s.rolling(window=20).std())
    df["BB_Middle"] = bb_mid
    df["BB_Upper"] = bb_mid + (2 * bb_std)
    df["BB_Lower"] = bb_mid - (2 * bb_std)

    # --- Target labels: shift(-1) pulls TOMORROW's value into TODAY's row ---
    # Grouped by Ticker so the last row of one stock never borrows the first
    # row of the next stock as its "tomorrow".
    df["Target_Price"] = grp["Close"].shift(-1)
    df["Target_Direction"] = (df["Target_Price"] > df["Close"]).astype(int)
    # Rows where Target_Price is NaN (the last day per ticker, with no "tomorrow")
    # will get Target_Direction=0 from the comparison above — fix that below,
    # since it's not a real "DOWN" label, it's just missing data.
    df.loc[df["Target_Price"].isna(), "Target_Direction"] = np.nan

    return df


def drop_incomplete_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows with any NaN feature/target values.
    These come from two sources:
      - Warm-up periods at the START of each ticker's history (rolling
        windows need N days of history before they're valid)
      - The very LAST day of each ticker's history (no "tomorrow" to
        form a target label from)
    """
    before = len(df)
    df = df.dropna().reset_index(drop=True)
    after = len(df)
    print(f"Dropped {before - after} incomplete rows ({before} -> {after})")
    return df


FEATURE_COLUMNS = [
    "Daily_Return", "EMA_20", "Volume_Momentum", "RSI_14",
    "MACD_Line", "MACD_Signal", "MACD_Histogram",
    "BB_Middle", "BB_Upper", "BB_Lower",
]


def scale_features(train_df: pd.DataFrame, test_df: pd.DataFrame, columns=FEATURE_COLUMNS):
    """
    Fit a StandardScaler on TRAIN data only, then apply it to both train
    and test. Call this from train.py AFTER the time-based split -
    never before, and never on the full dataset at once.

    Returns (train_scaled, test_scaled, fitted_scaler) so the scaler can
    also be saved alongside model.pkl for use at prediction time.
    """
    scaler = StandardScaler()
    train_scaled = train_df.copy()
    test_scaled = test_df.copy()
    train_scaled[columns] = scaler.fit_transform(train_df[columns])
    test_scaled[columns] = scaler.transform(test_df[columns])
    return train_scaled, test_scaled, scaler


def main():
    df = load_data()
    print(f"Loaded {len(df)} rows across {df['Ticker'].nunique()} tickers")

    df = add_features(df)
    df = drop_incomplete_rows(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved {len(df)} rows x {df.shape[1]} columns to {OUTPUT_PATH}")
    print(f"\nNOTE: features saved here are UNSCALED on purpose.")
    print(f"Call scale_features() from train.py AFTER the time-based split")
    print(f"to avoid leaking test-set statistics into training.")
    print()
    print(df[["Ticker", "Date", "Close", "RSI_14", "MACD_Histogram", "Target_Direction"]].head())


if __name__ == "__main__":
    main()
