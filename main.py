import os
import tweepy
import pandas as pd
import numpy as np
import GetOldTweets3 as got

client_key = os.environ['client_key']
client_secret = os.environ['client_secret']
bearer_token = os.environ['bearer_token']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']


def counter():
    my_file = open("counter.txt", "r+")
    counter = int(my_file.read()) + 1
    my_file.seek(0)
    my_file.write(str(counter))
    my_file.truncate()
    return counter


def is_retweet(x):
    if x.retweeted or "RT @" in x.full_text:
        return True
    return False


def is_comment(x):
    if x.full_text[0] == "@":
        return True
    return False


def get_profile_image(username):
    api = connect_to_twitter()
    cursor = tweepy.Cursor(api.user_timeline,
                           id=username,
                           tweet_mode='extended').items(1)
    for x in cursor:
        image_url = x.user.profile_image_url
    image_url = image_url.replace("_normal", "")
    return image_url


def connect_to_twitter():
    auth = tweepy.OAuthHandler(client_key, client_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def most_liked_tweets(username, how_many, min_likes):
    api = connect_to_twitter()
    cursor = tweepy.Cursor(api.user_timeline,
                           id=username,
                           tweet_mode='extended').items(how_many)
    tweets = []
    for x in cursor:
        if not is_retweet(x) and not is_comment(
                x) and x.favorite_count >= min_likes:
            favs = x.favorite_count
            retweets = x.retweet_count
            id = x.id
            when = x.created_at
            tweets.append([x.full_text, favs, retweets, id, when])
    tweet_df = pd.DataFrame(
        np.array(tweets), columns=['tweet', 'favs', 'retweets', 'id', 'date'])
    tweet_df.favs = tweet_df.favs.astype(int)
    tweet_df.retweet = tweet_df.retweet.astype(int)
    tweet_df = tweet_df.sort_values('favs',
                                    ascending=False).reset_index(drop=True)
    return tweet_df


def most_liked_tweets2(username, how_many, min_likes):
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(
        username).setMaxTweets(how_many)
    # Creation of list that contains all tweets
    thetweets = got.manager.TweetManager.getTweets(tweetCriteria)
    # Creating list of chosen tweet data
    tweets = []
    for x in thetweets:
        if not is_retweet(x) and not is_comment(
                x) and x.favorite_count >= min_likes:
            favs = x.favorite_count
            retweets = x.retweet_count
            id = x.id
            when = x.created_at
            tweets.append([x.full_text, favs, retweets, id, when])
    tweet_df = pd.DataFrame(
        np.array(tweets), columns=['tweet', 'favs', 'retweets', 'id', 'date'])
    tweet_df.favs = tweet_df.favs.astype(float)
    tweet_df.retweet = tweet_df.retweet.astype(float)
    tweet_df = tweet_df.sort_values('favs',
                                    ascending=False).reset_index(drop=True)
    return tweet_df


def export_janus_tweets(x, y):
    my_best_tweets = most_liked_tweets("JanuWaran", x, y)
    print(my_best_tweets.favs)
    the_counter = counter()
    my_best_tweets.to_csv('tweets' + str(the_counter) + '.csv', index=False)
    return the_counter


def tweets_to_images(file, username):
    tweets = pd.read_csv(file)
    profile_image = get_profile_image(username)
    for ind in tweets.index:
        tweet = tweets['tweet'][ind]
        favs = tweets['favs'][ind]
        retweets = tweets['retweets'][ind]
        date = tweets['date'][ind]
        # print(str(favs))
        # print(str(retweets))
        # print(date)


# export_janus_tweets(6701, 30)
tweets_to_images("tweets2.csv", "JanuWaran")
