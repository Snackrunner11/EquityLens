import streamlit as st
from data_loader import get_stock_data
from charts import create_chart

# List of symbols
STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", 
    "BTC-USD", "ETH-USD", "SPY", "QQQ", "AMD", "INTC", "DIS", "NKE", "SBUX",
    "SIE.DE", "BMW.DE", "VOW3.DE", "ALV.DE", "DTE.DE", "SAP.DE", "KO", "PEP"
]

def main():
    st.set_page_config("EquityLens", layout="wide")

    # Sidebar: Compact Inputs
    mode = st.sidebar.radio("Selection Mode", ["List", "Custom"], horizontal=True)
    if mode == "List":
        symbol = st.sidebar.selectbox("Stock", STOCKS)
    else:
        symbol = st.sidebar.text_input("Symbol", "AAPL").upper()
    
    period = st.sidebar.select_slider("Period", options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], value="1y")
    chart_type = st.sidebar.radio("Type", ["Candlestick", "Line"], horizontal=True)

    # Logic
    if symbol:
        df, info = get_stock_data(symbol, period)
        if df.empty:
            return st.error(f"No data for {symbol}")

        # Metrics
        st.title(info.get('longName', symbol))
        curr = df['Close'].iloc[-1]
        change = curr - df['Close'].iloc[-2]
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Price", f"{curr:.2f}", f"{change:.2f} ({change/df['Close'].iloc[-2]:.2%})")
        c2.metric("Mkt Cap", f"{info.get('marketCap', 0):,}")
        c3.metric("PE Ratio", info.get('trailingPE', 'N/A'))
        c4.metric("52W High", info.get('fiftyTwoWeekHigh', 'N/A'))

        # Visuals
        st.plotly_chart(create_chart(df, symbol, chart_type), use_container_width=True)
        
        with st.expander("Export Data"):
            st.download_button("Download CSV", df.to_csv(), f"{symbol}.csv", "text/csv")

if __name__ == "__main__":
    main()