import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_chart(df, symbol, chart_type):
    """Generates the Price and Volume chart."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)

    # 1. Price Trace
    if chart_type == "Candlestick":
        price_trace = go.Candlestick(x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close, name="OHLC")
    else:
        price_trace = go.Scatter(x=df.index, y=df.Close, name="Price")
    fig.add_trace(price_trace, row=1, col=1)

    # 2. Volume Trace
    colors = ['green' if c >= o else 'red' for c, o in zip(df.Close, df.Open)]
    fig.add_trace(go.Bar(x=df.index, y=df.Volume, marker_color=colors, name="Volume"), row=2, col=1)

    fig.update_layout(title=symbol, height=600, template="plotly_dark", xaxis_rangeslider_visible=False)
    return fig