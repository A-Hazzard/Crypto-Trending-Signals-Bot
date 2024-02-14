import pandas as pd
from indicators import calculate_ema_short, calculate_macd, calculate_rsi
from indicators import calculate_ema

rolling_data = {
    'close': [],  # Initialize with an empty list or preload with historical data
}

def update_rolling_data(new_close_price):
    global rolling_data
    # Add the new price to the rolling window and maintain its size
    rolling_data['close'].append(new_close_price)
    # Assume a window size, adjust based on your longest indicator lookback
    window_size = 200  
    rolling_data['close'] = rolling_data['close'][-window_size:]

def detect_signals(new_close_price, pair):
    # Update rolling data with the latest close price
    update_rolling_data(new_close_price)
    
    # Convert rolling data to DataFrame for compatibility with existing indicators
    df = pd.DataFrame(rolling_data)
    
    # Calculate indicators
    ema_short = calculate_ema_short(df['close'])
    ema_long = calculate_ema(df['close'])
    macd, signal_line, _ = calculate_macd(df['close'])
    rsi = calculate_rsi(df['close'])
    
    signals = []
    # Signal detection logic remains the same, adapted to the updated df
    if ema_short.iloc[-1] > ema_long.iloc[-1] and macd.iloc[-1] > signal_line.iloc[-1] and rsi.iloc[-1] < 70:
        signals.append(('BUY', "now"))  # "now" can be replaced with actual timestamp if needed

    if ema_short.iloc[-1] < ema_long.iloc[-1]:
        signals.append(('SELL', "now"))  # "now" can be replaced with actual timestamp if needed
    
    return signals
