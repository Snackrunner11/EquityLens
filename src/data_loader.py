import yfinance as yf
import streamlit as st

@st.cache_data
def get_stock_data(symbol: str, period: str):
    """Fetches both history and metadata in one go."""
    ticker = yf.Ticker(symbol)
    return ticker.history(period=period), ticker.info