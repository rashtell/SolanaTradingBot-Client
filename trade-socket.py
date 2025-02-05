import time
import asyncio
import requests
import websockets
import json
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
import config

# Solana RPC Client
client = Client(config.SOLANA_RPC_URL)

# Jupiter API Rate Limit Handling
JUPITER_RATE_LIMIT = 100  # 100 requests per minute
JUPITER_INTERVAL = 60 / JUPITER_RATE_LIMIT  # Throttle requests


async def get_token_market_cap():
    """Uses WebSocket to get real-time market cap updates."""
    async with websockets.connect(config.DEX_WEBSOCKET_URL) as ws:
        # Subscribe to the token's updates
        payload = json.dumps({"method": "subscribe", "params": [config.TOKEN_MINT]})
        await ws.send(payload)

        async for message in ws:
            data = json.loads(message)
            if "data" in data and "pairs" in data["data"]:
                market_cap = data["data"]["pairs"][0].get("fdv", 0)  # Fully Diluted Valuation
                return market_cap
            await asyncio.sleep(1)

def get_token_balance():
    """Fetches the wallet's token balance."""
    response = client.get_token_accounts_by_owner(Pubkey.from_string(config.WALLET_ADDRESS), {})
    for account in response["result"]["value"]:
        if account["account"]["data"]["parsed"]["info"]["mint"] == config.TOKEN_MINT:
            return int(account["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"])
    return 0

def execute_swap(input_token, output_token, amount, slippage_bps):
    """Performs a swap using Jupiter API with rate-limit handling and retries."""
    swap_url = f"{config.JUPITER_API}/quote"
    swap_params = {
        "inputMint": input_token,
        "outputMint": output_token,
        "amount": amount,
        "slippageBps": slippage_bps,
    }

    retry_count = 0
    while retry_count < 3:  # Retry up to 3 times on failure
        try:
            quote_response = requests.get(swap_url, params=swap_params).json()

            if "data" in quote_response:
                transaction = quote_response["data"]["swapTransaction"]
                signed_tx = Keypair.from_base58_string(config.PRIVATE_KEY).sign_message(transaction.encode())
                send_response = client.send_transaction(Transaction.deserialize(transaction.encode()), signed_tx)
                return send_response
            else:
                print("Invalid swap response, retrying...")
            
        except Exception as e:
            print(f"Swap failed: {e}, retrying...")
        
        retry_count += 1
        time.sleep(3)  # Wait before retrying
    
    print("Swap failed after 3 attempts.")
    return None

async def trade_logic():
    """Automates buy-sell logic using WebSocket updates and rate-limit handling."""
    while True:
        market_cap = await get_token_market_cap()
        print(f"Current Market Cap: ${market_cap}")

        if market_cap <= config.BUY_MARKET_CAP:
            print("Market cap is low, buying tokens...")
            execute_swap("So11111111111111111111111111111111111111112", config.TOKEN_MINT, config.AMOUNT, config.BUY_SLIPPAGE)
        
        elif market_cap >= config.SELL_MARKET_CAP and get_token_balance() > 0:
            print("Market cap is high, selling tokens...")
            execute_swap(config.TOKEN_MINT, "So11111111111111111111111111111111111111112", get_token_balance(), config.SELL_SLIPPAGE)

        await asyncio.sleep(JUPITER_INTERVAL)  # Respect Jupiter rate limits

# Start trading bot
asyncio.run(trade_logic())
