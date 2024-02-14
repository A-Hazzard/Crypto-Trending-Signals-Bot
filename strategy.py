from indicators import calculate_ema, calculate_macd, calculate_rsi
from signal_detector import detect_signals
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
def generate_signals(df, pair):
    logging.info(f"Looking for signals for pair: {pair}")

    initial_signals = detect_signals(df, pair)

    final_signals = []
    entry_ranges = []

    if not initial_signals:
            logging.info(f"No signals found for pair: {pair}\n------------------------------------\n")
    for signal in initial_signals:
        action, date = signal
        try:
            entry_price = df.loc[date, 'close']
            entry_low = entry_price * 0.98
            entry_high = entry_price * 1.02
            entry_ranges.append((pair, date, action, entry_low, entry_high))
            signal_details = create_signal(pair, action, entry_price)
            final_signals.append(signal_details)
        except KeyError:
            print(f"Date {date} not found in DataFrame index for {pair}.")

    return final_signals, entry_ranges

def create_signal(pair, signal_type, entry_price):
    # Adjust DCA, stop loss, and take profits dynamically based on the entry price
    dca_limit = entry_price * 0.98 if signal_type == "LONG" else entry_price * 1.02
    stop_loss = entry_price * 0.95 if signal_type == "LONG" else entry_price * 1.05
    take_profits = [entry_price * 1.05, entry_price * 1.10, entry_price * 1.15] if signal_type == "LONG" else [entry_price * 0.95, entry_price * 0.90, entry_price * 0.85]

    return {
        'pair': pair,
        'type': signal_type,
        'entry_price': f"{entry_price:.4f}",
        'dca_limit': f"{dca_limit:.4f}",
        'stop_loss': f"{stop_loss:.4f}",
        'take_profits': [f"{tp:.4f}" for tp in take_profits]
    }
