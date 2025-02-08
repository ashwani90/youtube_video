import tweepy

TWITTER_API_KEY = "your-twitter-api-key"
TWITTER_API_SECRET = "your-twitter-api-secret"
TWITTER_ACCESS_TOKEN = "your-access-token"
TWITTER_ACCESS_SECRET = "your-access-secret"

def post_to_twitter(tweet):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    
    api.update_status(tweet)
    print("✔ Posted to Twitter!")

# Example Usage
post_to_twitter("🚀 The stock market is booming! #Finance #StockMarket")
