import asyncio
import json
import websockets
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from notifier import send_discord_notification

async def process_signals(accumulated_data):
    """Process accumulated data for signals and send notifications."""
    if accumulated_data:
        logger.info("Processing signals based on accumulated data...")
        
        for data in accumulated_data:
            if 'k' not in data or 's' not in data:
                logger.warning("Skipping message without 'k' or 's' key.")
                continue

            signal_type = random.choice(['BUY', 'SELL'])
            latest_data = data
            signal = {
                'pair': latest_data['s'],
                'type': signal_type,
                'entry_range': latest_data['k']['c'],
                'dca_limit': float(latest_data['k']['c']) * 0.98,
                'stop_loss': float(latest_data['k']['c']) * 0.95,
                'take_profits': [float(latest_data['k']['c']) * 1.05,
                                 float(latest_data['k']['c']) * 1.10,
                                 float(latest_data['k']['c']) * 1.15]
            }
            try:
                send_discord_notification(signal)
                logger.info("Notification sent successfully!")
            except Exception as e:
                logger.error(f"Error sending notification: {e}")

async def consume_websocket(base_url):
    pairs = ["dydxusdt", "shibusdt", "galausdt", "ltcusdt"]

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
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=10)  # Timeout after 10 seconds
                message_data = json.loads(message)
                
                if 'result' in message_data or 'id' in message_data:
                    logger.info("Control message received, skipping: %s", message_data)
                    continue

                if 'k' in message_data and 's' in message_data:
                    accumulated_data.append(message_data)
                else:
                    logger.warning("Skipping message without 'k' or 's' key: %s", message_data)
                    continue

                current_time = asyncio.get_event_loop().time()
                if not immediate_processing_done or current_time - last_processed_time >= 5400:
                    logger.info("Searching for buy or sell signals...")
                    await process_signals(accumulated_data)
                    accumulated_data.clear()
                    last_processed_time = current_time
                    immediate_processing_done = True

            except asyncio.TimeoutError:
                logger.warning("WebSocket receive timed out.")
                # Implement reconnection logic here if needed
                pass
            except Exception as e:
                logger.error("Error in WebSocket communication: %s", e)
                # Implement error handling and reconnection logic here if needed
                pass

async def main():
    binance_ws_base_url = "wss://stream.binance.com:9443/ws"
    await consume_websocket(binance_ws_base_url)

if __name__ == "__main__":
    asyncio.run(main())
