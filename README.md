# Trend Signals Bot

Trend Signals Bot is a Python application for generating trading signals based on trend analysis of cryptocurrency pairs. It utilizes technical indicators to identify potential trends and provides signals for entering and exiting trades.

## Features

- Generates trading signals based on trend analysis.
- Supports customization of cryptocurrency pairs to monitor.
- Provides entry ranges for trading signals.
- Dynamically adjusts parameters based on market conditions.
- Insure you run the dockerfile on windows only or else you will have to adjust it
## Installation

1. Clone the repository:
```
git clone https://github.com/A-Hazzard/Crypto-Trending-Signals
```

2. Install the dependencies:
```
pip install -r requirements.txt
```

3. Set up API keys:
Create a `.env` file in the project root directory and add your Binance API key and secret:
```
BINANCE_API_KEY=<your-api-key>
BINANCE_API_SECRET=<your-api-secret>
DISCORD_WEBHOOK_URL=<your-discord-webhook-url>
```

## Usage

1. Adjust the list of cryptocurrency pairs to monitor:

Modify the `pairs` list in the `main.py` file to include the desired pairs.

2. Build the Docker image:
```
docker build -t trend-signals .
```

3. Run the Docker container:
```
docker run -d --name trend-signals-container trend-signals
```

## Customization

You can customize the list of cryptocurrency pairs to monitor by modifying the `pairs` list in the `main.py` file.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug fixes, please open an issue or submit a pull request.
