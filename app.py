from fastapi import FastAPI
import joblib
from data import get_data
from features import add_features

app = FastAPI(title="Trader AI")

pipe = joblib.load("models/trader_xgb.pkl")

@app.get("/")
def root():
    return {"message": "Trader AI backend is running. Use /recommend?ticker=AAPL"}

@app.get("/recommend")
def recommend(ticker: str = "AAPL"):
    df = add_features(get_data(ticker).tail(300))
    last = df.iloc[-1]

    x = last[["SMA20", "SMA100", "SMA200", "RSI", "ATR"]].to_frame().T
    prob = float(pipe.predict_proba(x)[0, 1])

    if prob > 0.6 and last["Close"] > last["SMA200"]:
        signal = "BUY"
    elif prob > 0.5:
        signal = "HOLD"
    else:
        signal = "SELL"

    stop = float(last["Close"]) - 1.5 * float(last["ATR"])

    return {
        "ticker": ticker,
        "signal": signal,
        "confidence": round(prob, 3),
        "close": float(last["Close"]),
        "sma200": float(last["SMA200"]),
        "atr": float(last["ATR"]),
        "proposed_stop": stop,
    }
