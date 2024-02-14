from binance.client import Client
import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
client = Client(api_key, api_secret)

def fetch_historical_data(pair, interval='5m', lookback='1 day ago UTC'):
    candles = client.get_historical_klines(pair, interval, lookback)
    df = pd.DataFrame(candles, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['close'] = pd.to_numeric(df['close'])
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df.set_index('open_time', inplace=True)
    return df[['close']]
