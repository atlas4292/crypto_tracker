def create_reddit_index(driver): 
    try:
        driver.query("CREATE INDEX IF NOT EXISTS idx_reddit_posts ON reddit_posts (id)")
        driver.query("CREATE INDEX IF NOT EXISTS idx_reddit_comments ON reddit_comments (id)")
    except:
        pass

def create_reddit_constraints(driver):
    """
    Create constraints for Reddit nodes to ensure uniqueness.
    """
    driver.query("CREATE CONSTRAINT IF NOT EXISTS FOR (n:RedditPost) REQUIRE n.id IS UNIQUE")
    driver.query("CREATE CONSTRAINT IF NOT EXISTS FOR (n:RedditComment) REQUIRE n.id IS UNIQUE")

def create_twitter_index(driver):
    try:
        driver.query("CREATE INDEX IF NOT EXISTS idx_twitter_posts ON twitter_posts (id)")
        driver.query("CREATE INDEX IF NOT EXISTS idx_twitter_users ON twitter_users (username)")
    except:
        pass

def create_twitter_constraints(driver):
    """
    Create constraints for Twitter nodes to ensure uniqueness.
    """
    driver.query("CREATE CONSTRAINT IF NOT EXISTS FOR (n:TwitterPost) REQUIRE n.id IS UNIQUE")
    driver.query("CREATE CONSTRAINT IF NOT EXISTS FOR (n:User) REQUIRE n.username IS UNIQUE")

def create_news_index(driver):
    try:
        driver.query("CREATE INDEX IF NOT EXISTS idx_news_articles ON news_articles (id)")
        driver.query("CREATE INDEX IF NOT EXISTS idx_news_sources ON news_sources (name)")
    except:
        pass

def create_news_constraints(driver):
    """
    Create constraints for News nodes to ensure uniqueness.
    """
    driver.query("CREATE CONSTRAINT IF NOT EXISTS FOR (n:NewsArticle) REQUIRE n.id IS UNIQUE")
    driver.query("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Source) REQUIRE n.name IS UNIQUE")

