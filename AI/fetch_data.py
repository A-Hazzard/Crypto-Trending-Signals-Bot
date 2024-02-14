import requests
import pandas as pd
from datetime import datetime

def fetch_binance_data(symbol, interval, start_str, end_str=None):
    url = 'https://api.binance.com/api/v3/klines'
    start_time = int(datetime.strptime(start_str, '%d %b %Y').timestamp() * 1000)
    end_time = int(datetime.strptime(end_str, '%d %b %Y').timestamp() * 1000) if end_str else None
    limit = 1000
    
    klines = []
    while True:
        params = {'symbol': symbol, 'interval': interval, 'startTime': start_time, 'limit': limit}
        if end_time:
            params['endTime'] = end_time
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception("API request error: " + response.text)
        data = response.json()
        if not data:
            break
        klines.extend(data)
        start_time = data[-1][0] + 1
        if end_time and start_time > end_time:
            break
    
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
               'quote_asset_volume', 'number_of_trades', 'taker_buy_base_volume',
               'taker_buy_quote_volume', 'ignore']
    df = pd.DataFrame(klines, columns=columns)
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    df['close'] = df['close'].astype(float)
    return df

if __name__ == "__main__":
    # Example usage
    df = fetch_binance_data('BTCUSDT', '1d', '1 Jan 2020', '1 Jan 2021')
    print(df.head())
