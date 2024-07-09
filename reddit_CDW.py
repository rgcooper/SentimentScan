import logging
import os
import json
import praw
from textblob import TextBlob
from collections import Counter
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Initialize Azure Key Vault
credential = DefaultAzureCredential()
key_vault_name = os.getenv('KEY_VAULT_NAME')
key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

# Get Reddit API credentials from Key Vault
client_id = secret_client.get_secret('reddit-client-id').value
client_secret = secret_client.get_secret('reddit-client-secret').value
user_agent = secret_client.get_secret('reddit-user-agent').value

# Authenticate with Reddit API
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

# Initialize Azure Blob Storage
blob_service_client = BlobServiceClient(account_url=os.getenv('AZURE_STORAGE_ACCOUNT_URL'), credential=credential)
container_client = blob_service_client.get_container_client('sentiment-analysis')

# Save results to Azure Blob Storage
blob_name = 'cdw_sentiment_analysis.json'
blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(json.dumps(post_data), overwrite=True)

# Example: Count the number of positive, negative, and neutral posts
sentiment_counter = Counter([data['sentiment'] for data in post_data])
logging.info(f"Sentiment Analysis:\n{sentiment_counter}")
