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

import time
import pandas as pd
import yfinance as yf
from pathlib import Path

# ---- CONFIG: Nifty 50 constituents (Yahoo Finance uses the .NS suffix for NSE) ----
# NOTE: Nifty 50 composition changes periodically (index rebalancing).
# Verify this list against the official NSE/Nifty Indices site before your final run:
# https://www.niftyindices.com/indices/equity/broad-based-indices/nifty-50
TICKERS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BHARTIARTL.NS",
    "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS",
    "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS", "INDUSINDBK.NS", "INFY.NS",
    "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS",
    "NTPC.NS", "NESTLEIND.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS",
    "SBILIFE.NS", "SHRIRAMFIN.NS", "SBIN.NS", "SUNPHARMA.NS", "TCS.NS",
    "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS", "TITAN.NS",
    "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS", "LTIM.NS", "BPCL.NS",
]
START_DATE = "2015-01-01"   # go back far enough for a meaningful dataset
END_DATE = None             # None = up to today
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5     # wait between retries if a download fails
REQUEST_DELAY_SECONDS = 1   # small pause between tickers to avoid rate-limiting

RAW_DATA_DIR = Path("data/raw")


def download_stock_data(ticker: str, start: str, end: str | None) -> pd.DataFrame:
    """Download OHLCV data for a single ticker, with retries."""
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Downloading {ticker} (attempt {attempt}/{MAX_RETRIES})...")
        df = yf.download(ticker, start=start, end=end, progress=False)

        if not df.empty:
            # yfinance sometimes returns a MultiIndex column header when downloading
            # a single ticker with certain versions — flatten it just in case.
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df = df.reset_index()  # turn the Date index into a normal column
            df["Ticker"] = ticker
            return df

        print(f"  No data returned for {ticker}, retrying in {RETRY_DELAY_SECONDS}s...")
        time.sleep(RETRY_DELAY_SECONDS)

    print(f"  WARNING: Failed to download {ticker} after {MAX_RETRIES} attempts. Skipping.")
    return pd.DataFrame()


def main():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_data = []
    failed_tickers = []
    for ticker in TICKERS:
        df = download_stock_data(ticker, START_DATE, END_DATE)
        if not df.empty:
            all_data.append(df)
        else:
            failed_tickers.append(ticker)
        time.sleep(REQUEST_DELAY_SECONDS)  # be polite to Yahoo's servers

    if failed_tickers:
        print(f"\nThe following {len(failed_tickers)} tickers failed and were skipped: {failed_tickers}")

    if not all_data:
        raise RuntimeError("No data was downloaded for any ticker. Check your internet connection or tickers.")

    combined = pd.concat(all_data, ignore_index=True)

    # Keep only the columns the project plan asks for
    combined = combined[["Date", "Open", "High", "Low", "Close", "Volume", "Ticker"]]

    output_path = RAW_DATA_DIR / "raw.csv"
    combined.to_csv(output_path, index=False)
    print(f"\nSaved {len(combined)} rows to {output_path}")
    print(combined.head())
z

if __name__ == "__main__":
    main()
