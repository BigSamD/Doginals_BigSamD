from bitcoinrpc.authproxy import AuthServiceProxy
from dotenv import load_dotenv
import os
import statistics

# Load environment variables
load_dotenv()

# Environment variables for RPC connection
NODE_RPC_URL = os.getenv("NODE_RPC_URL")
NODE_RPC_USER = os.getenv("NODE_RPC_USER")
NODE_RPC_PASS = os.getenv("NODE_RPC_PASS")
TESTNET = os.getenv("TESTNET") == "true"
NUM_BLOCKS = int(os.getenv("NUM_BLOCKS", 100))

def get_rpc_connection():
    """Create an RPC connection to the Dogecoin node."""
    rpc_url = f"http://{NODE_RPC_USER}:{NODE_RPC_PASS}@{NODE_RPC_URL.split('//')[-1]}"
    return AuthServiceProxy(rpc_url)

def get_recent_blocks_fee_info(rpc_connection, num_blocks=100):
    """Get transaction fee information from recent blocks."""
    best_block_hash = rpc_connection.getbestblockhash()
    fees = []
    for _ in range(num_blocks):
        block = rpc_connection.getblock(best_block_hash)
        # Iterate over transactions in the block, skipping the coinbase transaction
        for txid in block['tx'][1:]:
            try:
                tx_details = rpc_connection.getrawtransaction(txid, True)
                # Attempt to calculate the transaction fee
                if 'vin' in tx_details and 'vout' in tx_details:
                    # Sum the values of inputs and outputs to calculate the fee
                    input_sum = sum([vin['value'] for txin in tx_details['vin'] for vin in rpc_connection.getrawtransaction(txin['txid'], True)['vout'] if txin['vout'] == vin['n']])
                    output_sum = sum([vout['value'] for vout in tx_details['vout']])
                    fee = input_sum - output_sum
                    fees.append(fee)
            except Exception as e:
                print(f"Error obtaining transaction details: {e}")
        # Move to the previous block
        if 'previousblockhash' in block:
            best_block_hash = block['previousblockhash']
        else:
            break
    return fees

def estimate_fee(rpc_connection, num_blocks=100):
    """Estimate transaction fees based on analysis of recent blocks."""
    fees = get_recent_blocks_fee_info(rpc_connection, num_blocks)
    if fees:
        # Calculate the average fee from collected data
        average_fee = statistics.mean(fees)
        return average_fee
    return None

if __name__ == "__main__":
    rpc_connection = get_rpc_connection()
    estimated_fee = estimate_fee(rpc_connection, NUM_BLOCKS)
    if estimated_fee:
        print(f"Estimated fee: {estimated_fee} satoshis")
    else:
        print("Could not estimate fee.")
