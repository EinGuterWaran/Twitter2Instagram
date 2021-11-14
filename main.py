import fetch_tweets as ft
import tweet_image as ti

tweetlist_file = ft.tweets_to_csv("JanuWaran", 6701, 30)
ti.tweets_to_images(tweetlist_file, "JanuWaran", "Janu", True, True)
