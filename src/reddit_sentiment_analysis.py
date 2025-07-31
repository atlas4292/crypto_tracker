import praw
from utils import load_config
import uuid

TEST_REDDIT_POST_URL = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"

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
    
    def read_posts_comments(self, post_url):
        try:
            submission = self.reddit.submission(url=post_url)
            submission.comments.replace_more(limit=None)
            return [comment.body for comment in submission.comments.list()]
        except Exception as e:
            print(f"Failed to read posts/comments: {e}")
            return []


config = load_config()
reddit_client = RedditClient(config)
comments = reddit_client.read_posts_comments(TEST_REDDIT_POST_URL)
print(f"Comments from {TEST_REDDIT_POST_URL}:")
for comment in comments:
    print(comment)
