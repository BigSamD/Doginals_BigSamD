import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables from the .env file
load_dotenv()

# Environment variables
NODE_RPC_URL = os.getenv("NODE_RPC_URL")
NODE_RPC_USER = os.getenv("NODE_RPC_USER")
NODE_RPC_PASS = os.getenv("NODE_RPC_PASS")

# Configure the HTTP request header
headers = {
    'content-type': 'application/json',
}

def estimate_fee(priority):
    """
    Estimate fee based on the provided priority: low, medium, or high.
    The function sends a request to the node's RPC interface and prints out the estimated fee.
    """
    # Map priority to the number of blocks for estimation
    priority_mapping = {
        "low": 6,  # Estimate fee for lower priority (more blocks)
        "medium": 3,  # Estimate fee for medium priority
        "high": 1  # Estimate fee for high priority (next block)
    }
    blocks = priority_mapping.get(priority, 3)  # Default to medium if priority is not recognized

    # Prepare the request payload
    payload = json.dumps({
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": "estimatesmartfee",
        "params": [blocks]
    })

    # Make the RPC request
    response = requests.post(NODE_RPC_URL, auth=(NODE_RPC_USER, NODE_RPC_PASS), headers=headers, data=payload)

    # Process the response
    if response.status_code == 200:
        result = response.json()
        fee_rate = result['result']['feerate'] if 'feerate' in result['result'] else 'Not available'
        
        # Convert fee rate to Satoshis per KB for consistency
        satoshi_fee_rate = float(fee_rate) * 10**8 if fee_rate != 'Not available' else 'Not available'
        
        print(f"Estimated {priority} priority fee: {fee_rate} DOGE per KB")
        print(f"Equivalent in Satoshis per KB: {satoshi_fee_rate} sats per KB")
    else:
        print(f"Error calling estimatesmartfee for {priority} priority:", response.text)

# Example usage
priorities = ["low", "medium", "high"]
for priority in priorities:
    estimate_fee(priority)
