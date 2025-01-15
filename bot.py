from fetch_sales import fetch_sales
import tweepy
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Initialize Tweepy client
client = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_SECRET
)

# Track already-posted sales
posted_sales = set()

def post_to_twitter(nft_name, price, buyer, image_url):
    """Post a tweet with NFT sale details."""
    try:
        tweet = (
            f"🎉 New NFT Sale! 🎉\n\n"
            f"🔹 NFT Name: {nft_name}\n"
            f"💰 Price: {price} BTC\n"
            f"👤 Buyer: {buyer}\n"
            f"📸 Image: {image_url}\n\n"
            f"#PizzaPets #NFT #Bitcoin"
        )
        # Post the tweet
        response = client.create_tweet(text=tweet)
        print(f"Tweet posted successfully: {response.data['id']}")
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")

def process_sales(sales_data):
    """Process sales and post them to Twitter."""
    if not sales_data:
        print("No recent sales found.")
        return

    for sale in sales_data:
        nft_name = sale.get("tokenMint", "Unknown NFT")
        price = sale.get("price", "Unknown Price")
        buyer = sale.get("buyer", "Unknown Buyer")
        image_url = sale.get("image", "No Image Available")

        # Skip sales we've already posted
        if nft_name in posted_sales:
            print(f"Skipping already posted sale: {nft_name}")
            continue

        # Log sale details
        print("🚨 New NFT Sale Detected! 🚨")
        print(f"NFT Name: {nft_name}")
        print(f"Price: {price} BTC")
        print(f"Buyer: {buyer}")
        print(f"Image URL: {image_url}")
        print("-" * 40)

        # Post to Twitter
        post_to_twitter(nft_name, price, buyer, image_url)

        # Add sale to posted list
        posted_sales.add(nft_name)

def run_bot():
    """Run the bot continuously to check for new sales."""
    collection_symbol = "pizza-pets"  # Updated to the correct collection symbol
    print(f"Listening for sales on collection: {collection_symbol}")

    while True:
        # Fetch sales from the API
        sales_data = fetch_sales(collection_symbol)

        # Process the fetched sales data
        process_sales(sales_data)

        # Wait before polling again (e.g., 60 seconds)
        time.sleep(60)

if __name__ == "__main__":
    run_bot()