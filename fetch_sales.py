import requests
import time

# Base URL for Bitcoin Ordinals API
ORDINALS_API_URL = "https://api-mainnet.magiceden.dev/v2/ord/btc/activities"

def fetch_sales(collection_symbol):
    """Fetch recent buying_broadcasted activities for the specified Bitcoin Ordinals collection."""
    params = {
        "collectionSymbol": collection_symbol,  # Specify the collection
        "kind": "buying_broadcasted",  # Use the correct kind for sales
        "limit": 10  # Optional: Limit the number of results
    }
    print(f"Fetching from URL: {ORDINALS_API_URL} with params: {params}")
    try:
        response = requests.get(ORDINALS_API_URL, params=params)

        # Print the status code and raw response for debugging
        print(f"Status Code: {response.status_code}")
        print("Raw Response:", response.text)

        if response.status_code == 200:
            return response.json()  # Return JSON response
        elif response.status_code == 429:
            print("Rate limit exceeded. Retrying after 60 seconds...")
            time.sleep(60)  # Wait for 1 minute before retrying
            return fetch_sales(collection_symbol)  # Retry after waiting
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    collection_symbol = "pizza-pets"  # Set to the Pizza Pets collection symbol
    print("Fetching buying_broadcasted activities for:", collection_symbol)
    activities = fetch_sales(collection_symbol)

    if activities:
        print("Activities Data (First 5):", activities[:5])  # Print the first 5 activities for clarity
    else:
        print("No recent activities found for the collection.")