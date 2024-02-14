# from binance.client import Client
# import os
# import pandas as pd
# from dotenv import load_dotenv
# load_dotenv()  # This loads the variables from .env into the environment

# api_key = os.getenv('BINANCE_API_KEY')
# api_secret = os.getenv('BINANCE_API_SECRET')
# client = Client(api_key, api_secret)

# def fetch_historical_data(pair, interval='5m', lookback='1 day ago UTC'):
#     candles = client.get_historical_klines(pair, interval, lookback)
#     df = pd.DataFrame(candles, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
#     df['close'] = pd.to_numeric(df['close'])
#     df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
#     df.set_index('open_time', inplace=True)
#     return df[['close']]
import websocket
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def on_message(ws, message):
    message = json.loads(message)
    print("Received message:", message)
    # Process real-time data here. This might involve passing the data to your signal detection logic.

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("### WebSocket closed ###")

def on_open(ws):
    print("WebSocket opened")
    # Subscribe to candlestick data for specified pairs and intervals
    # Example: Subscribe to 1-minute candlesticks for BTCUSDT
    params = [
        "btcusdt@kline_1m",  # You can add more pairs here
    ]
    subscription_message = {
        "method": "SUBSCRIBE",
        "params": params,
        "id": 1
    }
    ws.send(json.dumps(subscription_message))

if __name__ == "__main__":
    # Define WebSocket URL for Binance
    binance_ws_url = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(binance_ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
