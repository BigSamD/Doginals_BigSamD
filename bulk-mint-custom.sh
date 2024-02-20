#!/bin/bash

# Check that 3 arguments are passed in, otherwise exit
if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ./bulk-mint-custom.sh <max_count> <target_address> <token_name>"
    exit 1
fi

# Initialize variables with command line arguments
count=0
max_count=$1
target_address=$2
token_name=$3
transaction_count=0

# Sync the wallet before starting the minting process
echo "Initial wallet sync..."
node . wallet sync
echo "Initial sync completed."

# Function to sync wallet and delete pending-txs.json
sync_and_cleanup() {
    echo "Syncing wallet..."
    node . wallet sync
    echo "Sync completed."

    # Attempt to delete pending-txs.json
    if [ -f "pending-txs.json" ]; then
        echo "Deleting pending-txs.json file..."
        rm -f "pending-txs.json" && echo "pending-txs.json deleted successfully." || echo "Failed to delete pending-txs.json."
    else
        echo "No pending-txs.json file to delete."
    fi
}

# Main loop for minting process
while [ $count -lt $max_count ]; do
    echo "Current count: $count"
    # Command for minting
    if node . drc-20 mint "$target_address" "$token_name" 100000000 5; then
        echo "Minting successful."
    else
        echo "Minting failed, possibly due to insufficient funds. Attempting to sync and clean up..."
        sync_and_cleanup
        echo "Resuming minting process..."
        continue  # Skip the rest of the loop and try minting the next item
    fi

    remaining=$((max_count - count))
    echo "Counts left: $remaining"
    sleep 10  # Sleep for 10 seconds, adjust as needed

    ((count++))
    ((transaction_count++))

    # Every 6 transactions, sync and clean up
    if [ "$transaction_count" -eq 6 ]; then
        sync_and_cleanup
        transaction_count=0  # Reset the transaction counter
    fi
done
