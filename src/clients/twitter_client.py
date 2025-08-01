import tweepy
from utils import load_config

class TwitterClient:
    def __init__(self, config):
        self.config = config
        self.client = tweepy.Client(
            bearer_token=config['twitter']['bearer_token'],
            consumer_key=config['twitter']['api_key'],
            consumer_secret=config['twitter']['api_secret_key'],
            access_token=config['twitter']['access_token'],
            access_token_secret=config['twitter']['access_token_secret']
        )

    def read_tweets(self, query, max_results=10):
        tweets = self.client.search_recent_tweets(query=query, max_results=max_results)
        return [tweet.text for tweet in tweets.data] if tweets.data else []

def test_twitter_client():
    """Test the Twitter client by reading recent tweets."""
    print("Testing Twitter Client...")
    try:
        config = load_config()
        twitter_client = TwitterClient(config)
        tweets = twitter_client.read_tweets("bitcoin", max_results=5)
        print("Recent Tweets about Bitcoin:")
        for tweet in tweets:
            print(tweet)
    except Exception as e:
        print(f"Error during Twitter client test: {e}")