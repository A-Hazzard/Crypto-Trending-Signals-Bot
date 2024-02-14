import pandas as pd
from indicators import calculate_ema_short
from indicators import calculate_ema

def detect_signals(df, pair):
    signals = []
    ema_short = calculate_ema_short(df['close'])
    ema_long = calculate_ema(df['close'])
    
    # Determine trend direction based on moving average crossover
    if ema_short.iloc[-1] > ema_long.iloc[-1] and ema_short.iloc[-2] <= ema_long.iloc[-2]:
        signals.append(('BUY', df.index[-1]))
    elif ema_short.iloc[-1] < ema_long.iloc[-1] and ema_short.iloc[-2] >= ema_long.iloc[-2]:
        signals.append(('SELL', df.index[-1]))
    
    return signals
