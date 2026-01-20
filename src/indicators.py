import pandas as pd

def calculate_technical_indicators(df):
    """
    Adds SMA, Bollinger Bands, RSI, and MACD columns to the dataframe.
    """
    data = df.copy()

    # SMA
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()

    # Bollinger Bands
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    data['STD20'] = data['Close'].rolling(window=20).std()
    data['BB_Upper'] = data['SMA20'] + (data['STD20'] * 2)
    data['BB_Lower'] = data['SMA20'] - (data['STD20'] * 2)

    # RSI
    delta_close = data['Close'].diff()
    gain = (delta_close.where(delta_close > 0, 0)).rolling(window=14).mean()
    loss = (-delta_close.where(delta_close < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    data['EMA12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA26'] = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = data['EMA12'] - data['EMA26']
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    return data