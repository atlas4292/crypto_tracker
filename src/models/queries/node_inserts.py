
def insert_reddit_post(driver, post):
    reddit_insertion_cypher = """
    WITH $post AS post
    MERGE (p:RedditPost {id: post.id})
    ON CREATE SET p.title = post.title, p.body = post.body, p.author = post.author, p.created_at = post.created_at, p.embedding = post.embedding                                
    WITH p, post
    UNWIND post.comments AS comment
    MERGE (c:RedditComment {id: comment.id})
    ON CREATE SET c.body = comment.body, c.author = comment.author, c.created_at = comment.created_at, c.embedding = comment.embedding
    MERGE (p)-[:HAS_COMMENT]->(c)
    WITH c, comment
    UNWIND comment.replies AS reply
    MERGE (r:RedditComment {id: reply.id})
    ON CREATE SET r.body = reply.body, r.author = reply.author, r.created_at = reply.created_at, r.embedding = reply.embedding
    MERGE (c)-[:HAS_REPLY]->(r)
    RETURN p, s, c, r
    """
    driver.query(reddit_insertion_cypher, {"post": post})

def insert_twitter_post(driver, post):
    twitter_insertion_cypher = """
    WITH $post AS post
    MERGE (t:TwitterPost {id: post.id})
    ON CREATE SET t.text = post.text, t.author = post.author, t.created_at = post.created_at, t.embedding = post.embedding
    MERGE (t)-[:POSTED_IN]->(post.hashtag)
    WITH t, post
    UNWIND post.replies AS reply
    MERGE (r:TwitterReply {id: reply.id})
    ON CREATE SET r.text = reply.text, r.author = reply.author, r.created_at = reply.created_at, r.embedding = reply.embedding
    MERGE (t)-[:HAS_REPLY]->(r)
    WITH r, reply
    MERGE (u:User {username: post.author})
    MERGE (t)-[:POSTED_BY]->(u)
    RETURN t, r, u
    """
    driver.query(twitter_insertion_cypher, {"post": post})

def insert_news_article(driver, article):
    news_outlet_insertion_cypher = """
    WITH $article AS article
    MERGE (a:NewsArticle {id: article.id})
    ON CREATE SET a.title = article.title, a.content = article.content, a.author = article.author, a.published_date = article.published_date, a.embedding = article.embedding
    MERGE (s:Publisher {name: article.source})
    MERGE (a)-[:PUBLISHED_BY]->(s)
    RETURN a, s
    """
    driver.query(news_outlet_insertion_cypher, {"article": article})