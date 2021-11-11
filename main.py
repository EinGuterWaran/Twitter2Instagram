import os
import tweepy
import pandas as pd
import numpy as np
import GetOldTweets3 as got
import random
from PIL import Image, ImageDraw, ImageOps, ImageFont
import urllib.request
import requests
import cv2

client_key = os.environ['client_key']
client_secret = os.environ['client_secret']
bearer_token = os.environ['bearer_token']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

color_codes = [[251, 57, 88], [255, 200, 56], [109, 201, 147], [69, 142, 255], [18, 86, 136]]


def circle_image(im):
    size = im.size
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output


def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()
    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent
    return (text_width, text_height)


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


def get_name(username):
    api = connect_to_twitter()
    cursor = tweepy.Cursor(api.user_timeline,
                           id=username,
                           tweet_mode='extended').items(1)
    for x in cursor:
        name = x.user.name
    return name


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
        media_url=[]
        if not is_retweet(x) and not is_comment(x) and x.favorite_count >= min_likes:
            if 'media' in x.entities:
              for media in x.extended_entities['media']:
                media_url.append(media['media_url'])
            favs = x.favorite_count
            retweets = x.retweet_count
            id = x.id
            when = x.created_at
            tweets.append([x.full_text, favs, retweets, id, when, media_url])
    tweet_df = pd.DataFrame(np.array(tweets), columns=['tweet', 'favs', 'retweets', 'id', 'date', 'media_url'])
    tweet_df.favs = tweet_df.favs.astype(int)
    tweet_df.retweets = tweet_df.retweets.astype(int)
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
    tweet_df.retweet = tweet_df.retweets.astype(float)
    tweet_df = tweet_df.sort_values('favs',
                                    ascending=False).reset_index(drop=True)
    return tweet_df


def export_janus_tweets(x, y):
    my_best_tweets = most_liked_tweets("JanuWaran", x, y)
    the_counter = counter()
    my_best_tweets.to_csv('tweet_lists/tweets' + str(the_counter) + '.csv', index=False)
    return the_counter


def tweets_to_images(file, handle, name, showFavsRt, show_date): 
    # let name empty for original name
    tweets = pd.read_csv(file)
    profile_image = get_profile_image(handle)
    if name == "":
        name = get_name(handle)
    color2 = color_codes[random.randint(0, len(color_codes) - 1)]
    for ind in tweets.index:
        tweet = tweets['tweet'][ind]
        favs = tweets['favs'][ind]
        retweets = tweets['retweets'][ind]
        tweet_timestamp = tweets['date'][ind]
        tweet_id = tweets['id'][ind]
        media_url = tweets['media_url'][ind]
        color = color_codes[random.randint(0, len(color_codes) - 1)]
        while color2 == color:
          color = color_codes[random.randint(0, len(color_codes) - 1)]
        color2 = color
        tweet_to_image(name, handle, showFavsRt, show_date, tweet, tweet_timestamp, favs, retweets, profile_image, tweet_id, media_url, color[0], color[1], color[2])


def tweet_to_image(name, username, showFavsRt, show_date, tweet, tweet_timestamp, favs, retweets, profile_image, tweet_id, media_url, r, g, b):
    words = tweet.split(" ")
    to_remove=[]
    tweet_lines = []
    rectangle_w = 0
    for word in words:
      if word.startswith("https://t.co"):
        response = requests.get(word)
        if not "photo" in response.url and not "video" in response.url:
          to_remove.append(word)
          continue
        to_remove.append(word)
    for tr in to_remove:  
      words.remove(tr)
    tweet = " ".join(words)
    media_url = media_url.replace("[","").replace("]","").replace("'","").split(",")
    medias = len(media_url)
    if medias == 1 and media_url[0] == "":
      medias = 0
    media_sizes = []
    for url in media_url:
      if url != "":
        urllib.request.urlretrieve(url, "1.png")
        im = cv2.imread('1.png').shape
        media_sizes.append([im[0], im[1]])
    for media_size in media_sizes:
      if media_size[1] > 850:
        how_smaller = 850/media_size[1]
        media_size[1] = 850
        media_size[0] = int(how_smaller*media_size[0])
      if media_size[0] > 400:
        how_smaller = 400/media_size[0]
        media_size[0] = 400
        media_size[1] = int(how_smaller*media_size[1])
    width = 1080
    height = 1080
    urllib.request.urlretrieve(profile_image, "p_img.png")
    profile_image = Image.open("p_img.png", 'r')
    profile_image = circle_image(profile_image)
    profile_image = profile_image.resize((180, 180))
    img = Image.new(mode="RGB", size=(width, height), color=(r, g, b))
    img_w, img_h = profile_image.size
    bg_w, bg_h = img.size
    # offset = ((bg_w - img_w) // 6, (bg_h - img_h) // 6)
    draw = ImageDraw.Draw(img)
    tw_font = ImageFont.truetype("fonts/HelveticaNeueLight.ttf", 40)
    name_font = ImageFont.truetype("fonts/HelveticaNeueBold.ttf", 40)
    username_font = ImageFont.truetype("fonts/HelveticaNeueMedium.ttf", 35)
    date_font = ImageFont.truetype("fonts/HelveticaNeueMedium.ttf", 30)

    tweet_size = get_text_dimensions(tweet, tw_font)
    tweet_w = (width-900) // 2
    tweet_h = (height-tweet_size[1]) // 2 + 50
    if medias == 1:
      media_offset_h = media_sizes[0][0]
    else:
      media_offset_h = 0
    if tweet_size[0] <= 900 and "\n" not in tweet:
      tweet_w = (width-tweet_size[0]) // 2
      tweet_h = (height-tweet_size[1]-media_offset_h) // 2 + 50
      if tweet_size[0] <= 700:
        tweet_w = (width-700) // 2
        tweet_h = (height-tweet_size[1] -media_offset_h) // 2 + 50
        draw.rectangle(((tweet_w-60, tweet_h-300),(tweet_w+700+60, tweet_h+tweet_size[1]+media_offset_h+200)), fill="white")
        rectangle_w = tweet_w+700+60
      else:
        draw.rectangle(((tweet_w-60, tweet_h-300),(tweet_w+tweet_size[0]+60, tweet_h+tweet_size[1]+media_offset_h+200)), fill="white")
        rectangle_w = tweet_w+tweet_size[0]+60
      draw.text((tweet_w, tweet_h),tweet,(0,0,0), font=tw_font)
    else:
      tweet = tweet.replace("\n", " \n ")
      tweet_words = tweet.split(" ")
      current_line = ""
      for word in tweet_words:
        if word == "":
          word = ""
        if word == "\n":
          tweet_lines.append(current_line)
          current_line = ""
          continue
        if word.startswith("https://t.co"):                    continue
        if current_line != "":
          filler = " "
        else: 
          filler = ""
        if current_line!="" and word!="" and get_text_dimensions(current_line+filler+word, tw_font)[0] > 900:
          tweet_lines.append(current_line)
          current_line = word
        else:
          current_line += filler + word
      if (len(current_line) > 0):
        tweet_lines.append(current_line)
      tweet_w = (width-900) // 2
      tweet_h = (height-(tweet_size[1]+15)*len(tweet_lines)-media_offset_h) // 2 + 50
      draw.rectangle(((tweet_w-60, tweet_h-300),(tweet_w+900+60, tweet_h+0+media_offset_h+(tweet_size[1]+15)*len(tweet_lines)+200)), fill="white")
      rectangle_w = tweet_w+900+60
      line_no = 0
      for tweet_line in tweet_lines:
        draw.text((tweet_w, tweet_h+(tweet_size[1]+15)*line_no),tweet_line,(0,0,0), font=tw_font)
        line_no += 1
    img.paste(profile_image, (tweet_w, tweet_h-250), profile_image)
    draw.text((tweet_w + 200, tweet_h-200),name,(0,0,0), font=name_font)
    draw.text((tweet_w + 200, tweet_h-140),"@"+username,(83,100,113),font=username_font)
    fr_offset = tweet_h+0+(tweet_size[1]+15)*(1+len(tweet_lines))
    if medias == 1:
        media = Image.open("1.png", 'r')
        media = media.resize((media_sizes[0][1], media_sizes[0][0]))
        img.paste(media, ((width-media_sizes[0][1]) // 2, tweet_h+0+(tweet_size[1]+15)*(1+len(tweet_lines))))
        fr_offset = tweet_h+0+(tweet_size[1]+15)*(1+len(tweet_lines))+media_sizes[0][0]+50
    if showFavsRt:
        rectangle_w = rectangle_w - (tweet_w-60)
        fav_img = Image.open("resources/fav.png", 'r')
        rt_img = Image.open("resources/rt.png", 'r')
        fav_img = fav_img.resize((50,50))
        rt_img = rt_img.resize((66,40))
        img.paste(fav_img, ((tweet_w-60)+int(rectangle_w*0.3),fr_offset+50), fav_img)
        img.paste(rt_img, ((tweet_w-60)+int(rectangle_w*0.6),fr_offset+50), rt_img)
        draw.text(((tweet_w-60)+int(rectangle_w*0.3)+70, fr_offset+50),str(favs),(0,0,0), font=username_font)
        draw.text(((tweet_w-60)+int(rectangle_w*0.6)+80, fr_offset+50),str(retweets),(0,0,0), font=username_font)
    if show_date:
        tweet_timestamp2 = tweet_timestamp.split("-")
        tweet_timestamp3 = tweet_timestamp2[2].split(" ")
        tweet_timestamp4 = tweet_timestamp3[1].split(":")
        months = ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]
        tweet_timestamp = tweet_timestamp4[0]+":"+tweet_timestamp4[1]+" "+tweet_timestamp3[0]+". "+months[int(tweet_timestamp2[1])+1]+" "+tweet_timestamp2[0]
        draw.text((tweet_w, fr_offset-20),tweet_timestamp,(83,100,113),font=date_font)
    img.save("tweet_images/" + str(tweet_id) + ".jpg")
    print("tweet_images/" + str(tweet_id) + ".jpg saved.")


# counter = export_janus_tweets(6701, 30)
# tweets_to_images("tweet_lists/tweets"+counter+".csv", "JanuWaran")
# export_janus_tweets(300,20)
tweets_to_images("tweet_lists/tweets2.csv", "JanuWaran", "Janu", True, True)
