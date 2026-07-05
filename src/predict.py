import numpy as np
import pandas as pd
import os

def make_prediction(data: pd.DataFrame, model=None) -> pd.DataFrame:
    """
    Generates next-day stock price predictions.
    If no trained model is provided, it applies a simple baseline (Moving Average).
    """
    df = data.copy()
    
    if model is None:
        # Day 2 Baseline Strategy: If Close price is above 5-day moving average, buy (1), else sell (-1)
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_5'] = df['MA_5'].bfill() 
        df['Predicted_Signal'] = np.where(df['Close'] > df['MA_5'], 1, -1)
    else:
        pass
        
    return df

if __name__ == "__main__":
    print("Testing predict.py engine with real cleaned data...")
    processed_data_path = "data/processed/clean.csv"
    
    if os.path.exists(processed_data_path):
        full_df = pd.read_csv(processed_data_path)
        
        # Pull a stock out of Sahil's new dataset to verify the metrics
        sample_ticker = "RELIANCE.NS"
        stock_df = full_df[full_df["Ticker"] == sample_ticker].copy()
        stock_df["Date"] = pd.to_datetime(stock_df["Date"])
        stock_df.set_index("Date", inplace=True)
        
        # Run prediction
        result_df = make_prediction(stock_df)
        print(f"\n--- Prediction Signals for {sample_ticker} ---")
        print(result_df[['Close', 'Predicted_Signal']].tail(10))
        
        # Import your backtester to immediately verify metrics
        from backtest import run_backtest
        metrics = run_backtest(result_df)
        print(f"\n--- Backtest Performance for {sample_ticker} ---")
        for key, val in metrics.items():
            print(f"{key}: {val}")
    else:
        print(f"Error: Could not find {processed_data_path}.")