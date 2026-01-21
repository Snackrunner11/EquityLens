# EquityLens

**EquityLens** is a Python based financial dashboard built with Streamlit. It allows users to visualize stock market data, analyze price trends, and monitor key financial metrics for various assets and cryptocurrencies.

## Features

* **Stock Selection**: Choose from a predefined list of popular assets (e.g., AAPL, TSLA, BTC USD, SIE.DE) or input a custom ticker symbol.
* **Interactive Charts**: Visualize data using dynamic Plotly charts. Switch between "Candlestick" and "Line" modes.
* **Volume Analysis**: View trading volume with color coded bars indicating price movement.
* **Key Metrics**: Automatically fetches and displays:
    * Current Price and Percentage Change
    * Market Capitalization
    * PE Ratio (Trailing)
    * 52 Week High
* **Adjustable Timeframes**: Analyze history ranging from 1 month to the maximum available data using a slider.
* **Data Export**: Download the analyzed historical data directly as a CSV file.

## Tech Stack

* **Python**: Core programming language.
* **Streamlit**: Web interface and interactivity.
* **yfinance**: Fetches historical market data and metadata.
* **Plotly**: Handles data visualization and graphing.

## Installation and Usage

1. Ensure you have Python installed.
2. Install the required dependencies:
    ```bash
    pip install streamlit yfinance plotly
    ```
3. Run the application:
    ```bash
    streamlit run src/main.py
    ```
