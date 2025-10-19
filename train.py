
# train.py
import os, joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV, TimeSeriesSplit
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import mlflow
import numpy as np
from data import get_data
from features import add_features

mlflow.autolog()   # auto-logs params, metrics, model

def main():
    print(">>> TRAIN START")

    # ---------- 1. data ----------
    print("Step 1/4: fetching AAPL data...")
    df = get_data("AAPL")
    print(f"downloaded {len(df):,} rows")

    print("Step 2/4: building features...")
    df = add_features(df)
    print(f"features ready, rows after dropna: {len(df):,}")

    # ---------- 2. split ----------
    X = df[["SMA20", "SMA100", "SMA200", "RSI", "ATR"]]
    y = df["Target"]

    print("Step 3/4: splitting and training...")
    Xtr, Xte, ytr, yte = train_test_split(X, y, shuffle=False, test_size=0.2)

    # ---------- 3. pipeline ----------
    pipe = Pipeline(steps=[
        ("scaler", StandardScaler()),
        ("clf",  XGBClassifier(
            n_estimators=400, max_depth=4, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, random_state=42,
            tree_method="hist", eval_metric="logloss"))
    ])

    # ---------- 4. hyper-parameter search (24 combos) ----------
    param_grid = {
        "clf__n_estimators": [200, 400, 800],
        "clf__max_depth":    [3, 4, 5],
        "clf__learning_rate": [0.01, 0.05, 0.1],
        "clf__subsample":    [0.8, 0.9, 1.0],
    }

    search = RandomizedSearchCV(
        pipe, param_grid,
        n_iter=24, cv=TimeSeriesSplit(n_splits=3),
        scoring="neg_log_loss", n_jobs=-1,
        random_state=42, verbose=1
    )

    search.fit(Xtr, ytr)
    acc = search.best_score_
    print(f"Best neg-log-loss: {acc:.3f}")

    # ---------- 5. save best model ----------
    os.makedirs("models", exist_ok=True)
    joblib.dump(search.best_estimator_, "models/trader_pipe.pkl")
    print("√ saved to models/trader_pipe.pkl")

if __name__ == "__main__":
    main()