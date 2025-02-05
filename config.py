import os
from dotenv import load_dotenv
import argparse


# Load environment variables from .env file
load_dotenv()

# Fetch values
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Validate variables
if not WALLET_ADDRESS or not PRIVATE_KEY:
    raise ValueError("Missing WALLET_ADDRESS or PRIVATE_KEY in .env file")

print(f"Wallet: {WALLET_ADDRESS[:6]}... Loaded Successfully")  # Masking for security

def get_args():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Solana Trading Bot")

    # Required argument
    parser.add_argument("TOKEN_MINT", type=str, nargs="?", help="Token mint address")
    parser.add_argument("--AMOUNT", type=float, required=True, help="Amount of SOL to swap")
    parser.add_argument("--BUY_MARKET_CAP", type=float, help="Buy when market cap reaches this value")
    parser.add_argument("--SELL_MARKET_CAP", type=float, help="Sell when market cap reaches this value")

    # Optional arguments with defaults
    parser.add_argument("--BUY_SLIPPAGE", type=float, default=2.0, help="Slippage tolerance for buying in percentage (default: 2%)")
    parser.add_argument("--SELL_SLIPPAGE", type=float, default=2.0, help="Slippage tolerance for selling in percentage (default: 2%)")

    # Parse arguments
    return parser.parse_args()

# Get parsed arguments
args = get_args()

# Validate TOKEN_MINT
if not args.TOKEN_MINT:
    parser.error("TOKEN_MINT is required. Usage: python bot.py <TOKEN_MINT> [options]")

# Store in variables
TOKEN_MINT = args.TOKEN_MINT
AMOUNT = args.AMOUNT  # SOL amount to buy with
BUY_MARKET_CAP = args.BUY_MARKET_CAP
SELL_MARKET_CAP = args.SELL_MARKET_CAP
BUY_SLIPPAGE = args.BUY_SLIPPAGE
SELL_SLIPPAGE = args.SELL_SLIPPAGE


# Print values (for debugging)
print(f"Token Mint: {TOKEN_MINT}")
print(f"Buy Market Cap: {BUY_MARKET_CAP}")
print(f"Sell Market Cap: {SELL_MARKET_CAP}")
print(f"Buy Slippage: {BUY_SLIPPAGE}%")
print(f"Sell Slippage: {SELL_SLIPPAGE}%")


SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"

# Jupiter Swap API (Solana's DEX aggregator)
JUPITER_API = "https://quote-api.jup.ag/v6"

# DexScreener WebSocket URL
DEX_WEBSOCKET_URL = "wss://io.dexscreener.com/dex/subscribe"
DEX_TOKEN_URL = f"https://api.dexscreener.io/latest/dex/tokens/{TOKEN_MINT}"