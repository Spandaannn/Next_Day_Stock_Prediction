"""
backtest.py
-----------
Simple backtesting engine that simulates a strategy driven by the model's
UP/DOWN predictions and compares it against Buy & Hold.

Owner: Person 2 (Software Engineer) — implemented on Day 4.

Strategy logic:
    - Prediction UP   -> Buy / hold position for that day
    - Prediction DOWN -> Stay in cash

Metrics to compute:
    - Portfolio value over time
    - Total return
    - Sharpe ratio
    - Max drawdown
    - Comparison vs Buy & Hold

Run:
    python src/backtest.py
"""

import pandas as pd
import numpy as np

def run_backtest(predictions: pd.DataFrame, initial_capital: float = 10000.0) -> dict:
    """
    Simulates trading based on 'Predicted_Signal' and calculates returns.
    
    Args:
        predictions (pd.DataFrame): Dataframe containing 'Close' prices and 'Predicted_Signal'.
        initial_capital (float): Starting cash balance.
        
    Returns:
        dict: Performance metrics (Total Return, Final Portfolio Value).
    """
    backtest_df = predictions.copy()
    
    # Calculate daily log returns of the stock
    backtest_df['Market_Returns'] = np.log(backtest_df['Close'] / backtest_df['Close'].shift(1))
    
    # Strategy returns = Signal from previous day multiplied by today's market return
    backtest_df['Strategy_Returns'] = backtest_df['Predicted_Signal'].shift(1) * backtest_df['Market_Returns']
    
    # Calculate cumulative returns
    backtest_df['Cumulative_Market'] = np.exp(backtest_df['Market_Returns'].cumsum())
    backtest_df['Cumulative_Strategy'] = np.exp(backtest_df['Strategy_Returns'].fillna(0).cumsum())
    
    # Portfolio values
    final_value = initial_capital * backtest_df['Cumulative_Strategy'].iloc[-1]
    total_return = (backtest_df['Cumulative_Strategy'].iloc[-1] - 1) * 100
    
    metrics = {
        "Initial Capital": initial_capital,
        "Final Portfolio Value": round(final_value, 2),
        "Total Strategy Return (%)": round(total_return, 2)
    }
    
    return metrics
