import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_main_chart(df, ticker_symbol, chart_type, show_sma, show_bb, show_rsi, show_macd):
    """
    Builds the interactive Plotly chart with subplots.
    """
    # Determine subplot layout dynamically
    rows = 2
    row_heights = [0.7, 0.3]
    specs = [[{"secondary_y": False}], [{"secondary_y": False}]]
    
    # Add a 3rd row if an oscillator is selected
    if show_rsi or show_macd:
        rows = 3
        row_heights = [0.6, 0.2, 0.2]
        specs.append([{"secondary_y": False}])

    fig = make_subplots(
        rows=rows, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.05, 
        row_heights=row_heights,
        specs=specs
    )

    # 1. Price Chart (Row 1)
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], 
            low=df['Low'], close=df['Close'], name="OHLC"
        ), row=1, col=1)
    else:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Close'], mode='lines', name="Price"
        ), row=1, col=1)

    # Overlays
    if show_sma:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], line=dict(color='orange', width=1), name="SMA 50"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA200'], line=dict(color='blue', width=1), name="SMA 200"), row=1, col=1)

    if show_bb:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], line=dict(color='gray', width=1, dash='dot'), name="BB Upper"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], line=dict(color='gray', width=1, dash='dot'), fill='tonexty', name="BB Lower"), row=1, col=1)

    # 2. Volume Chart (Row 2)
    colors = ['green' if row['Open'] - row['Close'] >= 0 else 'red' for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name="Volume"), row=2, col=1)

    # 3. Indicators (Row 3 - Optional)
    if rows == 3:
        if show_macd:
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], line=dict(color='purple'), name="MACD"), row=3, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['Signal_Line'], line=dict(color='orange'), name="Signal"), row=3, col=1)
        elif show_rsi:
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], line=dict(color='purple'), name="RSI"), row=3, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

    fig.update_layout(title=f"Analysis: {ticker_symbol}", xaxis_rangeslider_visible=False, height=800, template="plotly_dark")
    return fig