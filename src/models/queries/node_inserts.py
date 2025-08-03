
def insert_reddit_post(driver, post):
    query = """
    WITH $post AS post
    MERGE (p:RedditPost {id: post.id})
    ON CREATE SET p.title = post.title, p.body = post.body, p.author = post.author, p.created_at = post.created_at
    MERGE (s:Subreddit {name: post.subreddit})
    MERGE (p)-[:POSTED_IN]->(s)
    WITH p, post
    UNWIND post.comments AS comment
    MERGE (c:RedditComment {id: comment.id})
    ON CREATE SET c.body = comment.body, c.author = comment.author, c.created_at = comment.created_at
    MERGE (p)-[:HAS_COMMENT]->(c)
    WITH c, comment
    UNWIND comment.replies AS reply
    MERGE (r:RedditComment {id: reply.id})
    ON CREATE SET r.body = reply.body, r.author = reply.author, r.created_at = reply.created_at
    MERGE (c)-[:HAS_REPLY]->(r)
    RETURN p, c, r
    """
    driver.query(query, {"post": post})

def insert_twitter_post(driver, post):
    query = """
    WITH $post AS post
    MERGE (t:TwitterPost {id: post.id})
    ON CREATE SET t.text = post.text, t.author = post.author, t.created_at = post.created_at
    MERGE (u:User {username: post.author})
    MERGE (t)-[:POSTED_BY]->(u)
    RETURN t, u
    """
    driver.query(query, {"post": post})

def insert_news_article(driver, article):
    query = """
    WITH $article AS article
    MERGE (a:NewsArticle {id: article.id})
    ON CREATE SET a.title = article.title, a.content = article.content, a.author = article.author, a.published_at = article.published_at
    MERGE (s:Source {name: article.source})
    MERGE (a)-[:PUBLISHED_BY]->(s)
    RETURN a, s
    """
    driver.query(query, {"article": article})
