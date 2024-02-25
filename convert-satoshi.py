def doge_to_satoshi(doge_amount):
    # 1 Dogecoin = 100,000,000 Satoshi
    satoshi_per_doge = 100_000_000
    satoshi_amount = int(doge_amount * satoshi_per_doge)  # Convert to int to avoid decimal part
    return f"{doge_amount} DOGE is equal to {satoshi_amount} Satoshi."

# Example usage
doge_amount = 0.5
print(doge_to_satoshi(doge_amount))
