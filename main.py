import asyncio
import json
import os
import websockets  # Ensure this is installed
from dotenv import load_dotenv
import random  # For demonstration signal generation
from datetime import datetime, timezone

# Assuming you've imported your notifier correctly
from notifier import send_discord_notification

# Load environment variables
load_dotenv()

async def process_signals(accumulated_data):
    """Process accumulated data for signals and send notifications."""
    # Example signal generation logic (replace with your actual logic)
    if accumulated_data:  # Check if there's accumulated data to process
        print("Processing signals based on accumulated data...")
        
        # Demonstration: Randomly decide on a signal type
        signal_type = random.choice(['BUY', 'SELL'])
        # Construct a signal based on the latest data point
        latest_data = accumulated_data[-1]
        signal = {
            'pair': latest_data['s'],  # Symbol from the latest message
            'type': signal_type,
            'entry_range': latest_data['k']['c'],  # Closing price as entry range
            'dca_limit': float(latest_data['k']['c']) * 0.98,  # Example calculation
            'stop_loss': float(latest_data['k']['c']) * 0.95,  # Example calculation
            'take_profits': [float(latest_data['k']['c']) * 1.05,  # Example calculations
                             float(latest_data['k']['c']) * 1.10,
                             float(latest_data['k']['c']) * 1.15]
        }
        # Send a notification for the generated signal
        send_discord_notification(signal)
    else:
        print("No accumulated data to process. No signals found.")

async def consume_websocket(url):
    """Consume messages from a WebSocket connection and process data periodically."""
    async with websockets.connect(url) as ws:
        # Subscribe to the APTUSDT trading pair
        await ws.send(json.dumps({
            "method": "SUBSCRIBE",
            "params": ["aptusdt@kline_5m"],  # Subscribe to APTUSDT 1-minute candlesticks
            "id": 1
        }))

        accumulated_data = []
        last_processed_time = asyncio.get_event_loop().time()

        while True:
            message = await ws.recv()
            message_data = json.loads(message)
            # Using json.dumps to nicely format the output
            accumulated_data.append(message_data)

            # Process signals every 30 seconds
            if asyncio.get_event_loop().time() - last_processed_time >= 5400:  # 90 minutes * 60 seconds
                print("Searching for buy or sell signals...")
                await process_signals(accumulated_data)
                accumulated_data.clear()  # Reset accumulated data after processing
                last_processed_time = asyncio.get_event_loop().time()

async def main():
    binance_ws_url = "wss://stream.binance.com:9443/ws/aptusdt@kline_5m"
    await consume_websocket(binance_ws_url)

if __name__ == "__main__":
    asyncio.run(main())
