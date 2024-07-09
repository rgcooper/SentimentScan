import tweepy
from textblob import TextBlob

# Set up your Twitter API credentials
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

# Authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Function to get tweets and analyze sentiment
def get_tweets_and_analyze_sentiment(query, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en').items(count)
    tweet_data = []
    
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        sentiment = 'positive' if analysis.sentiment.polarity > 0 else 'negative' if analysis.sentiment.polarity < 0 else 'neutral'
        tweet_data.append({'tweet': tweet.text, 'sentiment': sentiment})
    
    return tweet_data

# Get and analyze tweets containing the word 'CDW'
query = 'CDW'
tweet_data = get_tweets_and_analyze_sentiment(query)

# Print the results
for data in tweet_data:
    print(f"Tweet: {data['tweet']}\nSentiment: {data['sentiment']}\n")

# Example: Count the number of positive, negative, and neutral tweets
from collections import Counter
sentiment_counter = Counter([data['sentiment'] for data in tweet_data])
print(f"Sentiment Analysis:\n{sentiment_counter}")
