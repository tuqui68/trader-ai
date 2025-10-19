import yfinance as yf
import pandas as pd

def get_data(ticker: str, start: str = "2015-01-01") -> pd.DataFrame:
    df = yf.download(ticker, start=start, auto_adjust=False, progress=False)
    df = df.rename(columns={"Adj Close": "AdjClose"})
    df = df[["Open", "High", "Low", "Close", "AdjClose", "Volume"]]
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
    return df