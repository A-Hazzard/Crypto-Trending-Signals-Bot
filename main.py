import os
import sys
import schedule
import time
import logging
from datetime import datetime

# Ensure the script directory is in sys.path
script_directory = os.path.dirname(os.path.abspath(__file__))
if script_directory not in sys.path:
    sys.path.append(script_directory)

from data_fetcher import fetch_historical_data
from strategy import generate_signals
from notifier import send_discord_notification

# Define the cryptocurrency pairs to monitor
pairs = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'LTCUSDT', 'BCHUSDT', 'BNBUSDT', 'LINKUSDT', 'XLMUSDT', 'VETUSDT', 'DOTUSDT', 'EOSUSDT', 'TRXUSDT', 'XMRUSDT', 'ATOMUSDT', 'UNIUSDT', 'AAVEUSDT', 'XTZUSDT', 'SOLUSDT']

def job():
    for pair in pairs:
        df = fetch_historical_data(pair)
        if df.empty:
            print(f"No data fetched for {pair}.")
            continue
        signals, entry_ranges = generate_signals(df, pair)
        for signal in signals:
            send_discord_notification(signal)

# Schedule the job function to run every hour
schedule.every(60).minutes.do(job)

if __name__ == "__main__":
    job()  # Run immediately before starting the scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)  # Adjust sleep time as needed to manage CPU usage