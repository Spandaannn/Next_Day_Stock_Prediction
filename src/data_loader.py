"""
data_loader.py
--------------
Day 1 task (Person 1): Download historical OHLCV data for chosen stocks
and save as raw.csv.

Concept notes:
- We use yfinance because it's free and needs no API key.
- For NSE (Indian) stocks, Yahoo Finance uses the ".NS" suffix
  (e.g., TCS.NS, INFY.NS, RELIANCE.NS, HDFCBANK.NS, ICICIBANK.NS).
- We pull a few years of daily data so later steps (moving averages,
  RSI, etc.) have enough history to compute correctly.
"""

import pandas as pd
import yfinance as yf
from pathlib import Path

# ---- CONFIG: edit this list to whichever stocks you want ----
TICKERS = ["TCS.NS", "INFY.NS", "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
START_DATE = "2015-01-01"   # go back far enough for a meaningful dataset
END_DATE = None             # None = up to today

RAW_DATA_DIR = Path("data/raw")


def download_stock_data(ticker: str, start: str, end: str | None) -> pd.DataFrame:
    """Download OHLCV data for a single ticker."""
    print(f"Downloading {ticker}...")
    df = yf.download(ticker, start=start, end=end, progress=False)

    if df.empty:
        print(f"  WARNING: No data returned for {ticker}. Check the ticker symbol.")
        return df

    # yfinance sometimes returns a MultiIndex column header when downloading
    # a single ticker with certain versions — flatten it just in case.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()  # turn the Date index into a normal column
    df["Ticker"] = ticker
    return df


def main():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_data = []
    for ticker in TICKERS:
        df = download_stock_data(ticker, START_DATE, END_DATE)
        if not df.empty:
            all_data.append(df)

    if not all_data:
        raise RuntimeError("No data was downloaded for any ticker. Check your internet connection or tickers.")

    combined = pd.concat(all_data, ignore_index=True)

    # Keep only the columns the project plan asks for
    combined = combined[["Date", "Open", "High", "Low", "Close", "Volume", "Ticker"]]

    output_path = RAW_DATA_DIR / "raw.csv"
    combined.to_csv(output_path, index=False)
    print(f"\nSaved {len(combined)} rows to {output_path}")
    print(combined.head())


if __name__ == "__main__":
    main()
