import requests
import os
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env into the environment

def send_discord_notification(signal):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if not webhook_url:
        print("Error: DISCORD_WEBHOOK_URL is not set.")
        return

    # Convert string to float for formatting, and back to string for message construction
    entry_range = f"{float(signal['entry_range']):.4f}"
    dca_limit = f"{float(signal['dca_limit']):.4f}"
    stop_loss = f"{float(signal['stop_loss']):.4f}"
    take_profits_formatted = [f"{float(tp):.4f}" for tp in signal['take_profits']]

    message = (
        f"------------------------------------\n"
        f"⚪ Trading pair: {signal['pair']}\n"
        f"⚪ Leverage: 10-25x\n"
        f"⚪ Type: {signal['type']}\n"
        f"⚪ Entry Range: {entry_range} (Market)\n"
        f"⚪ DCA LIMIT ORDER - {dca_limit}\n"
        f"⚪ Stop Loss - {stop_loss}\n"
        f"⚪ Take Profits: {', '.join(take_profits_formatted)}\n\n"
    )

    data = {"content": message}
    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print("Notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification: {e}")

