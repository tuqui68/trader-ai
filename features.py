import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Simple moving averages
    out["SMA20"]  = out["Close"].rolling(20).mean()
    out["SMA100"] = out["Close"].rolling(100).mean()
    out["SMA200"] = out["Close"].rolling(200).mean()

    # RSI(14), vanilla implementation
    delta = out["Close"].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / roll_down
    out["RSI"] = 100 - (100 / (1 + rs))

    # ATR(14), classic True Range then SMA
    h_l  = (out["High"] - out["Low"]).abs()
    h_pc = (out["High"] - out["Close"].shift(1)).abs()
    l_pc = (out["Low"]  - out["Close"].shift(1)).abs()
    tr = pd.concat([h_l, h_pc, l_pc], axis=1).max(axis=1)
    out["ATR"] = tr.rolling(14).mean()

    # Drop rows that don’t have indicators yet
    out = out.dropna().copy()
    return out
