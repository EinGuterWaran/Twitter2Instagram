import os
import tweepy
import pandas as pd
import numpy as np

client_key = os.environ['client_key']
client_secret = os.environ['client_secret']
bearer_token = os.environ['bearer_token']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']


def is_retweet(x):
    if x.retweeted or "RT @" in x.full_text:
        return True
    return False


def is_comment(x):
    if x.full_text[0] == "@":
        return True
    return False


auth = tweepy.OAuthHandler(client_key, client_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
cursor = tweepy.Cursor(api.user_timeline,
                       id='JanuWaran',
                       tweet_mode='extended').items(10000)
tweets = []
for x in cursor:
    if not is_retweet(x) and not is_comment(x) and x.favorite_count >= 10:
        favs = x.favorite_count
        retweets = x.retweet_count
        id = x.id
        when = x.created_at
        tweets.append([x.full_text, favs, retweets, id, when])
tweet_df = pd.DataFrame(np.array(tweets), columns=['tweet', 'favs', 'retweet', 'id', 'date'])
tweet_df.favs = tweet_df.favs.astype(float)
tweet_df.retweet = tweet_df.retweet.astype(float)
tweet_df = tweet_df.sort_values('favs', ascending=False).reset_index(drop=True)
print(tweet_df)
print(tweet_df.favs)
