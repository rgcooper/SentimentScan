import praw
from textblob import TextBlob
from collections import Counter

# Set up your Reddit API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
user_agent = 'your_user_agent'

# Authenticate with the Reddit API
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Function to get Reddit posts and analyze sentiment
def get_reddit_posts_and_analyze_sentiment(query, subreddit='all', limit=100):
    posts = reddit.subreddit(subreddit).search(query, limit=limit)
    post_data = []

    for post in posts:
        analysis = TextBlob(post.title)
        sentiment = 'positive' if analysis.sentiment.polarity > 0 else 'negative' if analysis.sentiment.polarity < 0 else 'neutral'
        post_data.append({'title': post.title, 'sentiment': sentiment})
    
    return post_data

# Get and analyze Reddit posts containing the word 'CDW'
query = 'CDW'
post_data = get_reddit_posts_and_analyze_sentiment(query)

# Print the results
for data in post_data:
    print(f"Post Title: {data['title']}\nSentiment: {data['sentiment']}\n")

# Example: Count the number of positive, negative, and neutral posts
sentiment_counter = Counter([data['sentiment'] for data in post_data])
print(f"Sentiment Analysis:\n{sentiment_counter}")
