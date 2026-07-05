# Stock Prediction Project Plan

Based on your proposal, your project is intentionally **MVP-first**:

Build a working stock direction prediction system in 5 days, then improve it into a production-worthy project with additional models, features, deployment, and optimization. Since there are 2 people, the best strategy is parallel development, not sequential work.

## Project Architecture

```
Historical Stock Data
          │
Data Collection Script
          │
Data Cleaning Pipeline
          │
Feature Engineering Module
          │
    ┌─────┴───────────────┐
    │                     │
Logistic Regression  Random Forest
    │                     │
    └─────┬───────────────┘
          │
   Model Evaluation
          │
Best Performing Model
          │
 Prediction Pipeline
          │
Simple Backtesting Engine
          │
Streamlit Dashboard (Optional)
```

## Technology Stack

### Programming
- Python

### Libraries
- pandas
- numpy
- scikit-learn
- matplotlib
- plotly
- yfinance (or NSE data)
- ta (technical indicators)
- joblib

### Optional
- Streamlit
- XGBoost
- LightGBM

## Folder Structure

```
StockPrediction/
│
├── data/
│      raw/
│      processed/
├── notebooks/
├── src/
│      data_loader.py
│      preprocess.py
│      features.py
│      train.py
│      predict.py
│      evaluate.py
│      backtest.py
├── models/
├── outputs/
│      graphs/
│      reports/
├── app/
│      streamlit_app.py
├── requirements.txt
└── README.md
```

## Team Division

### Person 1 (ML Engineer)
Responsible for everything related to Machine Learning.
- **Tasks**: Dataset collection, Data preprocessing, Feature engineering, Model training, Hyperparameter tuning, Evaluation, Model saving.

### Person 2 (Software Engineer)
Responsible for everything after the model.
- **Tasks**: Project structure, Prediction pipeline, Backtesting, Graphs, Streamlit dashboard, Documentation, GitHub management.

## 5-Day Roadmap

### DAY 1: Dataset and Project Skeleton
- **Person 1**: Download historical data (e.g., TCS, INFY, RELIANCE, HDFCBANK, ICICIBANK). Collect Date, Open, High, Low, Close, Volume. Save as `raw.csv`. Perform data cleaning (remove missing values, check duplicates, convert Date column, sort).
- **Person 2**: Create project folders, install packages, initialize Git, create `README`, `requirements.txt`, and Python files (`train.py`, `predict.py`, `evaluate.py`, `backtest.py`).
- **Deliverable**: Project skeleton, Dataset ready.

### DAY 2: Feature Engineering
- **Person 1**: Generate features (Daily Return, MA5, MA10, MA20, Rolling Volatility, RSI, MACD, Volume Change, Lag Returns). Create target (1 if tomorrow closes higher, 0 otherwise). Save `processed.csv`.
- **Person 2**: Create visualization scripts (Graphs for Price, Moving Average, Returns, Volume). Verify no future data leakage.
- **Deliverable**: Clean dataset, Feature dataset, Graphs.

### DAY 3: Model Training
- **Person 1**: Train Baseline (Logistic Regression) and Main (Random Forest). Evaluate (Accuracy, Precision, Recall, F1, Confusion Matrix, Feature Importance). Save model as `model.pkl`.
- **Person 2**: Implement prediction script (`predict.py`) to take latest stock data and output UP or DOWN.
- **Deliverable**: Working prediction system.

### DAY 4: Backtesting
- **Person 1**: Improve model (tune Random Forest: tree depth, number of estimators, feature selection).
- **Person 2**: Develop Backtesting Engine. Logic: Prediction UP = Buy, Prediction DOWN = Stay Cash. Calculate metrics (Portfolio value, Total Return, Sharpe Ratio, Max Drawdown). Compare Buy & Hold vs ML Strategy. Generate graphs.
- **Deliverable**: Model comparison, Backtesting, Performance plots.

### DAY 5: Integration
- **Person 1**: Testing, Bug fixing, Code cleanup, Model documentation.
- **Person 2**: (Optional) Build Streamlit App. Prepare presentation, README, Screenshots, Architecture diagram.
- **Deliverable**: Complete working MVP.

## Git Workflow
- `main`: Stable code
- `feature-ml`: Person 1
- `feature-app`: Person 2
- Merge into `main` every evening after testing.

## Minimum Viable Product (Must Have)
- ✅ Download stock data
- ✅ Clean data
- ✅ Feature engineering
- ✅ Logistic Regression
- ✅ Random Forest
- ✅ Next-day UP/DOWN prediction
- ✅ Evaluation metrics
- ✅ Backtesting
- ✅ Model saving/loading

## Phase 2 (After the Initial 5 Days)
| Priority | Feature | Why it helps |
| :--- | :--- | :--- |
| ⭐⭐⭐⭐⭐ | XGBoost/LightGBM | Usually stronger performance |
| ⭐⭐⭐⭐⭐ | Streamlit deployment | Interactive and presentation-ready |
| ⭐⭐⭐⭐ | Multiple stock support | Predict any Nifty 50 stock |
| ⭐⭐⭐⭐ | Automatic daily data updates | Keeps predictions current |
| ⭐⭐⭐⭐ | Hyperparameter optimization | Improves model quality |
| ⭐⭐⭐ | LSTM or GRU comparison | Demonstrates deep learning knowledge |
| ⭐⭐⭐ | News sentiment analysis | Adds fundamental context |
| ⭐⭐⭐ | SHAP explainability | Explains model predictions |
| ⭐⭐ | Portfolio recommendations | Extend beyond single-stock |
| ⭐⭐ | Docker + cloud deployment | Production-ready |
| ⭐⭐ | CI/CD with GitHub Actions | Shows software engineering practices |

## Project Guidelines
- **Keep the first version simple.**
- **Prevent data leakage.**
- **Use time-based splits** (train on earlier dates, test on later dates).
- **Commit to Git frequently.**
- **Document every experiment.**
- **Separate data, models, and code.**
- **Treat Day 5 as a freeze.** Focus on integration, testing, and presentation.
