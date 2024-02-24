import os
import requests
from dotenv import load_dotenv
from tqdm import tqdm

# Load variables from the .env file
load_dotenv()

# Retrieve variables for accessing the Dogecoin node from the .env file
rpc_url = os.getenv("NODE_RPC_URL")
rpc_user = os.getenv("NODE_RPC_USER")
rpc_pass = os.getenv("NODE_RPC_PASS")

# Create the authentication header for RPC calls
auth = (rpc_user, rpc_pass)

# Make an RPC call to the Dogecoin node
def call_rpc_method(method, params=[]):
    payload = {
        "method": method,
        "params": params,
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(rpc_url, json=payload, auth=auth)
    return response.json()

# Function to get the synchronization status
def get_sync_status():
    blockchain_info = call_rpc_method("getblockchaininfo")
    blocks_synced = blockchain_info["result"]["blocks"]
    blocks_total = blockchain_info["result"]["headers"]
    sync_percentage = (blocks_synced / blocks_total) * 100
    return sync_percentage

# Initialize the progress bar with the current synchronization status
sync_percentage = get_sync_status()
pbar = tqdm(total=100, initial=sync_percentage, desc="Synchronization Progress")

# Continuously update the progress bar until synchronization is complete
while sync_percentage < 100:
    sync_percentage = get_sync_status()
    pbar.n = sync_percentage
    pbar.refresh()
    pbar.set_postfix_str(f"Synchronization Progress: {sync_percentage:.2f}%")
    pbar.update(sync_percentage - pbar.n)

# Close the progress bar when synchronization is complete
pbar.n = 100
pbar.refresh()
pbar.close()
