import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data
def fetch_stock_data(symbol, period):
    """
    Fetches historical data and company info from Yahoo Finance.
    """
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period)
        info = ticker.info
        return history, info
    except Exception as e:
        return pd.DataFrame(), {}