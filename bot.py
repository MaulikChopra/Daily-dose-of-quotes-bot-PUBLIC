import tweepy
import json
import random
import os
import mongodb
""" ---- BOT.PY VERSION ONE ----"""
from dotenv import load_dotenv

load_dotenv()  # loads the env vairables


def authorization():
    try:
        dclient = tweepy.Client(
            # OAuth 1.0a
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_KEY_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            # OAuth 2.0
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN")
        )
        return dclient
    except Exception as e:
        print("client authorization Failed: ", e)
        return 1


"""---- MAKE THE TWEET CONTENT ----"""


def make_tweet():
    """ Gets quote raw and then make the proper tweet
    """
    def make_tagslist_to_tag(content, author, tagslist):
        quotetext = content + " - " + author + "\n" + "Tags:"
        for tag in tagslist:
            tag = tag.replace("-", "")
            quotetext += " #" + tag
        return quotetext

    print("generating tweet")
    quote_raw = __make_tweet_helper_mongodb()
    if quote_raw == 1:
        return 1
    else:
        content = quote_raw[0]
        author = quote_raw[1]
        tagslist = quote_raw[2]
        # join the tweet content
        quotetext = make_tagslist_to_tag(content, author, tagslist)
        if check_length_of_tweet(quotetext):
            print(quotetext)
            return quotetext
        else:
            print("Quote length too big ie: >280")
            make_tweet()


def __make_tweet_helper_mongodb():
    data = mongodb.get_random_quote()

    def filtered_tags(content, author, tagslist):
        quotetext = content + " - " + author + "\n" + "Tags:"
        l = []
        for tag in tagslist:
            if tag.count('-') < 2 and len(quotetext+tag) < 280:
                ftag = tag.replace("-", "").replace(" ", "")
                quotetext += " #"+ftag
                l.append(ftag)
        return l

    def filter_author(author):
        """removes everything right of "," """
        newauthor = ""
        for char in author:
            if char == ",":
                break
            newauthor += char
        return newauthor

    quote = data["Quote"]
    author = data["Author"]
    tags = data["Tags"]

    newauthor = filter_author(author)
    filteredtags = filtered_tags(quote, newauthor, tags)
    return quote, newauthor, filteredtags


def send_tweet(tweet, client):
    try:
        print("Posting tweet using client")
        client.create_tweet(text=tweet)
        print("tweet sent!")
        return 0
    except Exception as e:  # if error in tweet posting
        print("Client Tweet sending error:", e)
        return 1


def check_length_of_tweet(textoftweet):
    if len(textoftweet) >= 280:
        return False
    return True


""" --- BOT2.PY VERSION TWO TRACK TWEETS ---"""


def send_tweet_reply(client, textoftweet, tweet_id):
    client.create_tweet(text=textoftweet, in_reply_to_tweet_id=tweet_id)
    print("reply sent")


def get_latest_tweet(userid, client):
    """ Takes: id of user, client authorization
        Returns: tuple(tweet id, tweet text) """
    try:
        tweets = client.get_users_tweets(id=userid, max_results=5)
        return tweets.data[0].id, tweets.data[0].text
    except Exception as e:
        print(e)
        return -1
