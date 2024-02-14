from indicators import calculate_ema, calculate_macd, calculate_rsi
from signal_detector import detect_signals
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
def generate_signals(latest_close_price, pair):
    logging.info(f"Looking for signals for pair: {pair}")

    # Simulate detecting signals based on the latest price
    # This assumes detect_signals has been adapted to accept the latest price and pair as arguments
    initial_signals = detect_signals(latest_close_price, pair)  # Adjust the detect_signals function accordingly

    final_signals = []

    if not initial_signals:
        logging.info(f"No signals found for pair: {pair}\n------------------------------------\n")
        return final_signals

    for signal in initial_signals:
        action, _ = signal  # The second value is now ignored since we don't use date
        # Simplify signal creation based on the latest close price
        signal_details = create_signal(pair, action, latest_close_price)
        final_signals.append(signal_details)

    return final_signals

def create_signal(pair, signal_type, entry_price):
    # Adjust DCA, stop loss, and take profits dynamically based on the entry price
    dca_limit = entry_price * 0.98 if signal_type == "LONG" else entry_price * 1.02
    stop_loss = entry_price * 0.95 if signal_type == "LONG" else entry_price * 1.05
    take_profits = [entry_price * 1.05, entry_price * 1.10, entry_price * 1.15] if signal_type == "LONG" else [entry_price * 0.95, entry_price * 0.90, entry_price * 0.85]

    # Construct and return the signal dictionary
    return {
        'pair': pair,
        'type': signal_type,
        'entry_price': f"{entry_price:.4f}",
        'entry_range': f"{entry_price:.4f}",  # Assuming entry_range is similar to entry_price for simplicity
        'dca_limit': f"{dca_limit:.4f}",
        'stop_loss': f"{stop_loss:.4f}",
        'take_profits': [f"{tp:.4f}" for tp in take_profits]
    }
