import fetch_tweets as ft
from PostOnInstagram import post_on_instagram as poi
from Tweet2Image import tweet_image as ti
import os


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
        mode = input("Enter L if you want to generate a list of the best tweets from an account!\n"
                     "Enter LI if you additionally want to generate Instagram worthy images from these tweets!\n"
                     "Enter I if you want to generate Instagram worthy images from an existing list!\n"
                     "Enter P if you want to post a tweet image on Instagram!\n")
        if mode in ["L", "l", "LI", "li", "I", "i", "P", "p"]:
            break
    if mode not in ["p", "P"]:
        while True:
            twitter_handle = input("Enter the Twitter username (handle)! ")
            if twitter_handle != "":
                break
            print("Your input is empty.")
        twitter_name = input(
            "Enter the name (leave this blank if you want to fetch the original name)! "
        )
    if mode not in ["I", "i", "P", "p"]:
        while True:
            last_x_tweets = input(
                "How many recent tweets should be reviewed (Leave empty to use the maximum possible number)? "
            )
            if last_x_tweets == "" or checkIfNumber(last_x_tweets):
                if last_x_tweets == "":
                    last_x_tweets = 6701
                break
        while True:
            min_favs = input("How many likes should the tweets have minimally? ")
            if checkIfNumber(min_favs):
                break
        tweetlist_file = ft.tweets_to_csv(twitter_handle, int(last_x_tweets),
                                          int(min_favs))
        if mode in ["LI", "li"]:
            ti.tweets_to_images(tweetlist_file, twitter_handle, twitter_name, True, True)
    if mode in ['I', 'i']:
        filename = input("Enter the file name (without the csv ending)!\n")
        filename = 'tweet_lists/' + twitter_handle + '/' + filename + '.csv'
        ti.tweets_to_images(filename, twitter_handle, twitter_name, True,
                            True)
    if mode in ['P', 'p']:
        filename = input("Enter the file name of the image (without the jpg ending)!\n")
        username = input("Enter your Instagram username!\n")
        password = input("Enter your Instagram password!\n")
        caption = input("Enter the caption for the post!\n")
        try:
            print("Posting...")
            dir_path = os.path.dirname(os.path.realpath(__file__))
            poi.post(username, password, dir_path+"\\tweet_images\\" + filename+".jpg", caption)
            print("Posted successfully.")
        except:
            print("The login failed. Check your username and password!")


if __name__ == "__main__":
    # command_line_interface()
    ti.tweets_to_images("tweet_lists/JanuWaran/tweets_JanuWaran_6701_25_2021-11-23_17-20-54.csv", "JanuWaran", "Janu", True, True)
    # tweetlist_file = ft.tweets_to_csv("matze_emmo",6701,1000)
    # TODO automatisierte Pipeline
    # TODO Wenn Bilder, sollen diese auch mit gespeichert + gepostet werden - Dateiname mit suffix
    # TODO Submodule (Fetch Tweets)
