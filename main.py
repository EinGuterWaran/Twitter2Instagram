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
        mode = input("Enter L if you want to generate a list of the best tweets from an account!\n"
                     "Enter LI if you additionally want to generate Instagram worthy images from these tweets!\n"
                     "Enter I if you want to generate Instagram worthy images from an existing list!\n")
        if mode in ["L", "l", "LI", "li", "I", "i"]:
            break
    while True:
        twitter_handle = input("Enter the Twitter username (handle)! ")
        if twitter_handle != "":
            break
        print("Your input is empty.")
    twitter_name = input(
        "Enter the name (leave this blank if you want to fetch the original name)! "
    )
    if mode not in ["i", "I"]:
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
        filename = 'tweet_lists/'+twitter_handle+'/'+filename+'.csv'
        ti.tweets_to_images(filename, twitter_handle, twitter_name, True,
                            True)


if __name__ == "__main__":
    command_line_interface()
    # tweetlist_file = ft.tweets_to_csv("matze_emmo",6701,1000)
    # TODO In CMD soll angezeigt werden was gerade passiert
    # TODO automatisierte Pipeline + Instagram Post (Facebook Graph API)
    # TODO Wenn Bilder, sollen diese auch mit gespeichert + gepostet werden - Dateiname mit suffix
