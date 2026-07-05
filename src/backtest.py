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

import numpy as np
import pandas as pd
from pathlib import Path

GRAPHS_DIR = Path("outputs/graphs")


def run_backtest(df: pd.DataFrame, predictions: pd.Series, initial_capital: float = 100_000.0) -> pd.DataFrame:
    """
    Simulate the ML strategy vs Buy & Hold.

    df must contain a 'Close' (or daily return) column aligned with `predictions`.
    """
    # TODO (Person 2): implement on Day 4
    raise NotImplementedError("run_backtest: to be implemented on Day 4")


def compute_metrics(portfolio_values: pd.Series) -> dict:
    """Total return, Sharpe ratio, max drawdown."""
    # TODO (Person 2): implement on Day 4
    raise NotImplementedError("compute_metrics: to be implemented on Day 4")


def plot_comparison(strategy_values: pd.Series, buy_hold_values: pd.Series, out_name: str = "backtest_comparison.png"):
    """Plot ML strategy vs Buy & Hold portfolio value over time."""
    # TODO (Person 2): implement on Day 4
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError("plot_comparison: to be implemented on Day 4")


if __name__ == "__main__":
    print("backtest.py scaffold ready — implement steps above on Day 4.")
