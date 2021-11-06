import os
import tweepy
import pandas as pd

client_key = os.environ['client_key']
client_secret = os.environ['client_secret']
bearer_token = os.environ['bearer_token']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

auth = tweepy.OAuthHandler(client_key, client_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
cursor = tweepy.Cursor(api.user_timeline, id='JanuWaran', tweet_mode='extended').items(1)
for x in cursor:
  print(dir(x))