import time
import requests
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
import config;

# Solana RPC Client
client = Client(config.SOLANA_RPC_URL)

def get_token_market_cap():
    """Fetches the market cap of the token from DexScreener API."""
    response = requests.get(config.DEX_TOKEN_URL).json()
    
    # Extract market cap (if available)
    if "pairs" in response and response["pairs"]:
        market_cap = response["pairs"][0].get("fdv", 0)  # Fully Diluted Valuation
        return market_cap
    return 0

def get_token_balance():
    """Fetches the balance of the token in the wallet."""
    response = client.get_token_accounts_by_owner(Pubkey.from_string(config.WALLET_ADDRESS), {})
    for account in response["result"]["value"]:
        if account["account"]["data"]["parsed"]["info"]["mint"] == config.TOKEN_MINT:
            return int(account["account"]["data"]["parsed"]["info"]["tokenAmount"]["amount"])
    return 0

def execute_swap(input_token, output_token, amount, slippage_bps):
    """Executes a token swap using Jupiter API with custom slippage."""
    swap_url = f"{config.JUPITER_API}/quote"
    swap_params = {
        "inputMint": input_token,
        "outputMint": output_token,
        "amount": amount,
        "slippageBps": slippage_bps,
    }
    
    quote_response = requests.get(swap_url, params=swap_params).json()
    
    if "data" in quote_response:
        transaction = quote_response["data"]["swapTransaction"]
        signed_tx = Keypair.from_base58_string(config.PRIVATE_KEY).sign_message(transaction.encode())
        send_response = client.send_transaction(Transaction.deserialize(transaction.encode()), signed_tx)
        return send_response
    return None

def trade_logic():
    """Automates the buy-sell loop based on market cap thresholds with custom slippage."""
    while True:
        market_cap = get_token_market_cap()
        print(f"Current Market Cap: ${market_cap}")

        if market_cap <= config.BUY_MARKET_CAP:
            print("Market cap is low, buying tokens...")
            execute_swap("So11111111111111111111111111111111111111112", config.TOKEN_MINT, config.AMOUNT, config.BUY_SLIPPAGE)  # Buy with custom slippage
        
        elif market_cap >= config.SELL_MARKET_CAP and get_token_balance() > 0:
            print("Market cap is high, selling tokens...")
            execute_swap(config.TOKEN_MINT, "So11111111111111111111111111111111111111112", get_token_balance(), config.SELL_SLIPPAGE)  # Sell with custom slippage

        time.sleep(60)  # Wait 1 minute before checking again

# Start trading bot
trade_logic()
