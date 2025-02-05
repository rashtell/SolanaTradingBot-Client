# Solana Trading Bot

This repository contains two versions of a Solana trading bot:

1. **API Pull Version (`trade-api.py`)** - Uses REST API requests to fetch token prices and execute trades.
2. **WebSocket Version (`trade-socket.py`)** - Uses WebSockets for real-time price updates and instant trade execution.

---

## Features

✅ Automatically buys a token when it reaches a specified market cap.
✅ Sells when the market cap hits a defined profit target.
✅ Supports custom slippage settings for buying and selling.
✅ Reads wallet credentials from a `.env` file.
✅ Allows command-line arguments for flexible configuration.

---

## Installation

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/your-repo/trading-bot.git
cd trading-bot
```

### 2️⃣ Install Dependencies

Ensure you have Python installed, then install required dependencies:

```sh
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file and add:

```
WALLET_ADDRESS=your_wallet_address
PRIVATE_KEY=your_private_key
```

---

## Usage

### **API Pull Version (`trade-api.py`)**

This version checks token prices at regular intervals using REST API requests.

**Run the bot:**

```sh
python trade-api.py <TOKEN_MINT> --AMOUNT <SOL_AMOUNT> --BUY_MARKET_CAP 15000000 --SELL_MARKET_CAP 25000000 --BUY_SLIPPAGE 2.0 --SELL_SLIPPAGE 2.0
```

**Example:**

```sh
python trade-api.py HsXhds23... --AMOUNT 1.0 --BUY_MARKET_CAP 15000000 --SELL_MARKET_CAP 25000000
```

### **WebSocket Version (`trade-socket.py`)**

This version listens for live price updates via WebSockets and executes trades instantly when conditions are met.

**Run the bot:**

```sh
python trade-socket.py <TOKEN_MINT> --AMOUNT <SOL_AMOUNT> --BUY_MARKET_CAP 15000000 --SELL_MARKET_CAP 25000000 --BUY_SLIPPAGE 2.0 --SELL_SLIPPAGE 2.0
```

**Example:**

```sh
python trade-socket.py HsXhds23... --AMOUNT 1.0 --BUY_MARKET_CAP 15000000 --SELL_MARKET_CAP 25000000
```

---

## Configuration Options

| Argument            | Description                        | Default |
| ------------------- | ---------------------------------- | ------- |
| `TOKEN_MINT`        | Token mint address (Required)      | None    |
| `--AMOUNT`          | Amount of SOL to trade (Required)  | None    |
| `--BUY_MARKET_CAP`  | Market cap to trigger buy order    | 15M     |
| `--SELL_MARKET_CAP` | Market cap to trigger sell order   | 25M     |
| `--BUY_SLIPPAGE`    | Slippage tolerance for buying (%)  | 2.0     |
| `--SELL_SLIPPAGE`   | Slippage tolerance for selling (%) | 2.0     |

---

## API Rate Limits

- **Dexscreener**: [Check Docs](https://docs.dexscreener.com/)
- **Jupiter**: [Check Docs](https://docs.jup.ag/)

---

## Notes

- The **WebSocket version (`trade-socket.py`)** is faster but requires a stable connection.
- The **API pull version (`trade-api.py`)** is more reliable but slightly slower due to request intervals.
- **Use at your own risk!** Crypto trading involves risks, and you should test with small amounts first.

---

## Future Enhancements

🔹 Add Telegram notifications for trade execution.
🔹 Implement stop-loss and trailing profit features.
🔹 Support multiple trading pairs in a single instance.

---

## License

This project is licensed under the MIT License.

---

## Disclaimer

This bot is for educational purposes only. The developers are not responsible for any financial losses.
