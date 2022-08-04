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


"""======== DEPRECEATED ======="""

# def make_tweet_helper_JSONdatabase():

#     def filtered_tags(content, author, tagslist):
#         quotetext = content + " - " + author + "\n" + "Tags:"
#         l = []
#         for tag in tagslist:
#             if tag.count('-') < 2 and len(quotetext+tag) < 280:
#                 ftag = tag.replace("-", "").replace(" ", "")
#                 quotetext += " #"+ftag
#                 l.append(ftag)
#         return l

#     with open("database/quotes.json", "r") as file:
#         data = json.load(file)

#     index = random.randrange(48391)
#     print("Quote index:", index)
#     quote = data[index]["Quote"]
#     author = data[index]["Author"]
#     newauthor = ""
#     for char in author:
#         if char == ",":
#             break
#         newauthor += char
#     tags = data[index]["Tags"]
#     filteredtags = filtered_tags(quote, newauthor, tags)
#     return quote, newauthor, filteredtags


# def make_tweet_helper_getquote():

#     # 50% chance of either directy calling the random method
#     # or calling the random tag method with random tag getter.

#     seed = random.randint(0, 1)
#     random_tag_list = ["business", "education", "faith", "famous-quotes", "friendship", "future", "happiness", "history", "inspirational",
#                        "life", "literature", "love", "nature", "politics", "proverb", "religion", "science", "success", "technology", "wisdom"]
#     if seed == 0:
#         randomtag = random.choices(random_tag_list, k=1)
#     # get the quote raw
#         try:
#             newQuote = GetQuote.RandomTag(randomtag)
#             content = newQuote.content()
#             author = newQuote.author()
#             tagslist = newQuote.tags()
#             return content, author, tagslist
#         except Exception as e:
#             print("tweet generation failed", e)
#             return 1

#     if seed == 1:
#         try:
#             newQuote = GetQuote.Random()
#             content = newQuote.content()
#             author = newQuote.author()
#             tagslist = newQuote.tags()
#             return content, author, tagslist
#         except Exception as e:
#             print("tweet generation failed", e)
#             return 1


# def make_tweet_helper_50kDatabase():
#     import csv
#     with open("database/50kDatabase.csv", "r") as file:
#         reader = csv.reader(file)
#         # max == 45575 lines/quotes
#         index = random.randrange(45576)
#         counter = 0
#         for row in reader:
#             counter += 1
#             if counter == index:
#                 return row[0], row[1], [row[2]]
# def read_ID_cache(user):  # REDUNDANT
#     with open("database/ID.json", "r") as file:
#         data = json.load(file)
#     return int(data[user])


# def load_IDjson():  # REDUNDANT
#     with open("database/ID.json", "r") as jfile:
#         data = json.load(jfile)
#     return data


# def write_ID_cache(user, tweet_id):  # REDUNDANT
#     data = load_IDjson()
#     data[user] = tweet_id
#     with open("database/ID.json", "w") as newfile:
#         json.dump(data, newfile)


# def load_github_IDjson():
#     data = decrypt_githubPAT()
#     g = Github(data)
#     repo = g.get_user().get_repo('Daily-dose-of-quotes-bot')
#     filepath = "database/ID.json"
#     gfile = repo.get_contents(
#         filepath, ref="v3-50Kjson-autoreply").decoded_content.decode()
#     content = json.loads(gfile)
#     return content


# def read_github_IDjson(user):
#     data = decrypt_githubPAT()
#     g = Github(data)
#     repo = g.get_user().get_repo('Daily-dose-of-quotes-bot')
#     filepath = "database/ID.json"
#     gfile = repo.get_contents(
#         filepath, ref="v3-50Kjson-autoreply").decoded_content.decode()
#     content = json.loads(gfile)
#     return int(content[user])


# def write_github_IDjson(user, tweet_id):
#     data = decrypt_githubPAT()
#     g = Github(data)
#     repo = g.get_user().get_repo('Daily-dose-of-quotes-bot')
#     tempdata = repo.get_contents(
#         "database/ID.json", ref="v3-50Kjson-autoreply")
#     data = tempdata.decoded_content.decode()
#     content = json.loads(data)
#     # update dict
#     content[user] = tweet_id
#     # convert back to json
#     jsondata = json.dumps(content)
#     # push to github
#     repo.update_file("database/ID.json",
#                      "from heroku server: "+user, jsondata, tempdata.sha, branch="v3-50Kjson-autoreply")


# write_github_IDjson("JeffBezos", 1)
# print(read_github_IDjson("chopra_maulik"))
