import praw
from utils import load_config
import uuid

TEST_REDDIT_POST_URL = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
# r/cryptocurrency, r/bitcoin

class RedditClient:
    def __init__(self, config):
        self.state = uuid.uuid4()
        self.reddit = praw.Reddit(
            client_id=config['reddit']['client_id'],
            client_secret=config['reddit']['client_secret'],
            redirect_uri=config['reddit']['redirect_uri'],
            user_agent=config['reddit']['user_agent']
        )

    def get_auth_url(self):
        return self.reddit.auth.url(scopes=["read", "identity"], state=self.state, duration="permanent")

    def authenticate(self, code):
        try:
            self.reddit.auth.authorize(code)
            return self.reddit.user.me()
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None
    
    def read_posts_comments(self, post_url, limit=10):
        try:
            submission = self.reddit.submission(url=post_url)
            submission.comments.replace_more(limit=limit)
            return [comment.body for comment in submission.comments.list()]
        except Exception as e:
            print(f"Failed to read posts/comments: {e}")
            return []
    
    def get_hottest_subreddit_submissions(self, subreddit_names, limit=10):
        try:
            subreddit = self.reddit.subreddit('+'.join(subreddit_names))
            return {submission.id: {"title": submission.title, "score": submission.score, "url": submission.url} for submission in subreddit.hot(limit=limit)}
        except Exception as e:
            print(f"Failed to get subreddit submission data: {e}")
            return {}


def test_reddit_client_comments():
    """Test the Reddit client by reading comments from a sample post."""
    print("Testing Reddit Client...")
    try:
        config = load_config()
        reddit_client = RedditClient(config)
        comments = reddit_client.read_posts_comments(TEST_REDDIT_POST_URL)
        print(f"Comments from {TEST_REDDIT_POST_URL}:")
        for comment in comments:
            print(comment)
    except Exception as e:
        print(f"Error during Reddit client test: {e}")

def test_reddit_subbreddits():
    """Test the Reddit client by fetching hottest submissions from specified subreddits."""
    print("Testing Reddit Client for Subreddits...")
    try:
        config = load_config()
        reddit_client = RedditClient(config)
        subreddit_info = reddit_client.get_hottest_subreddit_submissions(['cryptocurrency', 'bitcoin'])
        for submission in subreddit_info.values():
            print(f"Title: {submission['title']}, Score: {submission['score']}, URL: {submission['url']}")

    except Exception as e:
        print(f"Error during subreddit test: {e}")

if __name__ == "__main__":
    test_reddit_client_comments()
    test_reddit_subbreddits()
