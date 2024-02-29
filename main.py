import asyncio
import json
import websockets  # Ensure this is installed
import random  # For demonstration signal generation

# Assuming you've imported your notifier correctly
from notifier import send_discord_notification

async def process_signals(accumulated_data):
    """Process accumulated data for signals and send notifications."""
    if accumulated_data:  # Check if there's accumulated data to process
        print("Processing signals based on accumulated data...")
        
        for data in accumulated_data:
            # Skip messages that do not contain expected keys
            if 'k' not in data or 's' not in data:
                print("Skipping message without 'k' or 's' key.")
                continue

            # Use data safely after confirming its structure
            signal_type = random.choice(['BUY', 'SELL'])
            latest_data = data  # Use the validated data
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
            try:
                send_discord_notification(signal)
                print("Notification sent successfully!") # Log here on success
            except Exception as e:
                print(f"Error sending notification: {e}")

async def consume_websocket(base_url):
    pairs = ["ordiusdt", "rifusdt", "avaxusdt", "ensusdt", "ctsiusdt", "acheusdt"]

    async with websockets.connect(base_url) as ws:
        params = [f"{pair}@kline_5m" for pair in pairs]
        subscribe_message = json.dumps({
            "method": "SUBSCRIBE",
            "params": params,
            "id": 1
        })
        await ws.send(subscribe_message)

        accumulated_data = []
        last_processed_time = asyncio.get_event_loop().time()
        immediate_processing_done = False

        while True:
            message = await ws.recv()
            message_data = json.loads(message)

            # Check if message is a control message (e.g., subscription confirmation)
            if 'result' in message_data or 'id' in message_data:
                print("Control message received, skipping: ", message_data)
                continue  # Skip processing for control messages

            # Check if message has the expected structure before appending
            if 'k' in message_data and 's' in message_data:
                accumulated_data.append(message_data)
            else:
                print("Skipping message without 'k' or 's' key: ", message_data)
                continue  # Skip to the next message

            # Immediate and periodic processing logic here (unchanged)
            current_time = asyncio.get_event_loop().time()
            if not immediate_processing_done or current_time - last_processed_time >= 5400:
                print("Searching for buy or sell signals...")
                await process_signals(accumulated_data)
                accumulated_data.clear()
                last_processed_time = current_time
                immediate_processing_done = True

async def main():
    binance_ws_base_url = "wss://stream.binance.com:9443/ws"
    await consume_websocket(binance_ws_base_url)

if __name__ == "__main__":
    asyncio.run(main())
