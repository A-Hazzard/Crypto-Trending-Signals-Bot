from fetch_data import fetch_binance_data
from indicators import calculate_ema, calculate_macd, calculate_rsi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetch Data
df = fetch_binance_data('BTCUSDT', '1d', '1 Jan 2020', '1 Jan 2021')

# Convert 'close' to numeric, if it's not already
df['close'] = pd.to_numeric(df['close'])

# Calculate Indicators
df['EMA50'] = calculate_ema(df['close'], 50)
df['EMA200'] = calculate_ema(df['close'], 200)
macd_line, signal_line, macd_histogram = calculate_macd(df['close'])  # Adjust this line
df['MACD_Line'] = macd_line
df['Signal_Line'] = signal_line
df['MACD_Histogram'] = macd_histogram  # If you're calculating and using the histogram
df['RSI'] = calculate_rsi(df['close'])

# Define Signals based on your strategy (adjust according to your strategy)
df['Signal'] = 0
df.loc[df['EMA50'] > df['EMA200'], 'Signal'] = 1
df.loc[df['EMA50'] < df['EMA200'], 'Signal'] = -1

# Backtest Strategy
initial_capital = 10000.0
df['Position'] = df['Signal'].shift()
df['Market Returns'] = df['close'].pct_change()
df['Strategy Returns'] = df['Market Returns'] * df['Position']
df['Equity Curve'] = initial_capital * (1 + df['Strategy Returns'].cumsum())

# Plot the equity curve
plt.figure(figsize=(10, 6))
plt.plot(df['Equity Curve'], label='Equity Curve')
plt.title('Backtest Results')
plt.legend()
plt.show()
