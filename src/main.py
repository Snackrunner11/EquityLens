import streamlit as st
from data_loader import fetch_stock_data
from indicators import calculate_technical_indicators
from charts import create_main_chart

# Page Config
st.set_page_config(page_title="EquityLens Dashboard", layout="wide")

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")

# 1. Stock Selection (Hybrid Approach)
st.sidebar.subheader("Select Stock")

# Predefined list for quick access
STOCK_LIST = [
    "AAPL - Apple Inc.", "MSFT - Microsoft Corp.", "GOOGL - Alphabet Inc.",
    "AMZN - Amazon.com", "TSLA - Tesla Inc.", "NVDA - NVIDIA Corp.",
    "META - Meta Platforms", "NFLX - Netflix", "KO - Coca-Cola",
    "PEP - PepsiCo", "SIE.DE - Siemens AG", "BMW.DE - BMW AG",
    "VOW3.DE - Volkswagen AG", "ALV.DE - Allianz SE", "DTE.DE - Deutsche Telekom",
    "SAP.DE - SAP SE", "BTC-USD - Bitcoin", "ETH-USD - Ethereum",
    "SPY - S&P 500 ETF", "QQQ - Nasdaq 100 ETF", "AMD - AMD",
    "INTC - Intel", "DIS - Walt Disney", "NKE - Nike", "SBUX - Starbucks"
]

selected_stock = st.sidebar.selectbox("Quick Select:", STOCK_LIST)
custom_ticker = st.sidebar.text_input("Or enter symbol (e.g. RBLX):").upper().strip()

# Priority: Use custom text if provided, otherwise use dropdown
if custom_ticker:
    ticker_symbol = custom_ticker
else:
    ticker_symbol = selected_stock.split(" - ")[0]

# 2. Chart Settings
time_period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3)
chart_type = st.sidebar.radio("Chart Type", ["Candlestick", "Line"])

# 3. Indicators
st.sidebar.subheader("Technical Indicators")
show_sma = st.sidebar.checkbox("SMA (50 & 200)")
show_bb = st.sidebar.checkbox("Bollinger Bands")
show_rsi = st.sidebar.checkbox("RSI")
show_macd = st.sidebar.checkbox("MACD")

# --- Main Application Logic ---
if ticker_symbol:
    # Fetch Data
    df_raw, info = fetch_stock_data(ticker_symbol, time_period)

    if df_raw.empty:
        st.error(f"No data found for '{ticker_symbol}'. Please check the symbol.")
    else:
        # Process Data
        df_processed = calculate_technical_indicators(df_raw)

        # Header & Metrics
        st.title(f"{info.get('longName', ticker_symbol)}")
        
        current_price = df_processed['Close'].iloc[-1]
        prev_close = df_processed['Close'].iloc[-2]
        delta = current_price - prev_close
        delta_pct = (delta / prev_close) * 100

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Price", f"{current_price:.2f} {info.get('currency', 'USD')}", f"{delta:.2f} ({delta_pct:.2f}%)")
        col2.metric("Market Cap", f"{info.get('marketCap', 'N/A'):,}")
        col3.metric("PE Ratio", info.get('trailingPE', 'N/A'))
        col4.metric("52W High", info.get('fiftyTwoWeekHigh', 'N/A'))

        # Render Chart
        fig = create_main_chart(
            df_processed, ticker_symbol, chart_type, 
            show_sma, show_bb, show_rsi, show_macd
        )
        st.plotly_chart(fig, use_container_width=True)

        # Data Export
        with st.expander("Raw Data & Export"):
            st.dataframe(df_processed.tail())
            st.download_button(
                label="Download CSV",
                data=df_processed.to_csv().encode('utf-8'),
                file_name=f"{ticker_symbol}.csv",
                mime="text/csv"
            )