import streamlit as st
from data_loader import fetch_stock_data
from indicators import calculate_technical_indicators
from charts import create_main_chart

# Config
st.set_page_config(page_title="EquityLens Dashboard", layout="wide")

# Sidebar
st.sidebar.header("Configuration")
ticker_symbol = st.sidebar.text_input("Ticker Symbol", value="AAPL").upper()
time_period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3)
chart_type = st.sidebar.radio("Chart Type", ["Candlestick", "Line"])

st.sidebar.subheader("Technical Indicators")
show_sma = st.sidebar.checkbox("SMA (50 & 200)")
show_bb = st.sidebar.checkbox("Bollinger Bands")
show_rsi = st.sidebar.checkbox("RSI")
show_macd = st.sidebar.checkbox("MACD")

# Execution
if ticker_symbol:
    # 1. Get Data
    df_raw, info = fetch_stock_data(ticker_symbol, time_period)

    if df_raw.empty:
        st.error(f"No data found for {ticker_symbol}.")
    else:
        # 2. Process Data
        df_processed = calculate_technical_indicators(df_raw)

        # 3. Display KPIs
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

        # 4. Display Chart
        fig = create_main_chart(
            df_processed, ticker_symbol, chart_type, 
            show_sma, show_bb, show_rsi, show_macd
        )
        st.plotly_chart(fig, use_container_width=True)

        # 5. Export
        with st.expander("Raw Data"):
            st.dataframe(df_processed.tail())
            st.download_button("Download CSV", df_processed.to_csv().encode('utf-8'), f"{ticker_symbol}.csv", "text/csv")