# app_ui.py
import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Trader-AI Dashboard", layout="centered")

st.title("Trader-AI Dashboard")
st.markdown("---")

col1, col2 = st.columns([2, 1])
with col1:
    ticker = st.text_input("Ticker symbol", "AAPL").upper()
with col2:
    if st.button("Get Signal", type="primary"):
        with st.spinner("Fetching AI signal..."):
            r = requests.get(f"http://localhost:8000/recommend?ticker={ticker}")
            data = r.json()

        st.success("Done!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Signal", data["signal"])
        c2.metric("Confidence", f"{data['confidence']:.1%}")
        c3.metric("Stop Loss", f"${data['proposed_stop']:.2f}")

        df = yf.download(ticker, period="1mo", interval="1d")
        fig = go.Figure(data=go.Candlestick(
            x=df.index,
            open=df.Open,
            high=df.High,
            low=df.Low,
            close=df.Close,
            name="Candlesticks"
        ))
        fig.update_layout(title=f"{ticker} – Last Month", xaxis_title="Date", yaxis_title="Price ($)")
        st.plotly_chart(fig, use_container_width=True)