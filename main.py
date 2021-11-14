import fetch_tweets as ft
import tweet_image as ti


def checkIfNumber(number):
    try:
        int(number)
        return True
    except ValueError:
        print("This is not a number. Try it again!")
        return False


def janus_tweets():
    tweetlist_file = ft.tweets_to_csv("JanuWaran", 6701, 30)
    ti.tweets_to_images(tweetlist_file, "JanuWaran", "Janu", True, True)


def command_line_interface():
    while True:
        twitter_handle = input("Enter the Twitter username (handle)! ")
        if twitter_handle != "":
            break
        print("Your input is empty.")
    twitter_name = input(
        "Enter the name (leave this blank if you want to fetch the original name)! "
    )
    while True:
        last_x_tweets = input(
            "How many recent tweets should be reviewed (Leave empty to use the maximum possible number)? "
        )
        if (last_x_tweets == "" or checkIfNumber(last_x_tweets)):
            if last_x_tweets == "":
                last_x_tweets = 6701
            break
    while True:
        min_favs = input("How many likes should the tweets have minimally? ")
        if checkIfNumber(min_favs):
            break
    tweetlist_file = ft.tweets_to_csv(twitter_handle, int(last_x_tweets), int(min_favs))
    ti.tweets_to_images(tweetlist_file, twitter_handle, twitter_name, True,
                        True)


command_line_interface()
