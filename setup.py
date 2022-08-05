import threading
import time
from bot import *


def main(time_interval):
    """SENDS QUOTE EVERY 2 HOURS"""
    while True:
        client = authorization()
        if client != 1:  # if no error in authorization
            tweet = make_tweet()
            if tweet != 1:  # if no error in tweet generation
                sent = send_tweet(tweet, client)
                if sent != 1:  # if tweet sent, wait till next
                    time.sleep(time_interval)
                else:  # if error in sending tweet
                    time.sleep(10)
        print("-------------------------------")


def testing_main(time_interval):

    client = authorization()
    if client != 1:  # if no error in authorization
        tweet = make_tweet()
    print("-------------------------------")


def main_v2(tt):
    """REPLY TO THE LATEST TWEET OF PEOPLE IN ID.json"""
    while True:
        try:
            jsondata = mongodb.get_ID()
            client = authorization()
            if client != 1:  # if no error in authorization
                for user in jsondata.keys():
                    tweet = get_latest_tweet(int(user), client)
                    tweet_id = tweet[0]
                    if tweet != -1:
                        print("user: ", user, "tweetid: ", tweet_id)
                        id_in_file = mongodb.get_ID(user=user)
                        if tweet_id != id_in_file:
                            texttweet = make_tweet()
                            send_tweet_reply(client, texttweet, tweet_id)
                            if mongodb.write_ID(user, tweet_id) == 0:
                                print(
                                    tweet_id, "updated on mongodb altas: quotes.id")
                            time.sleep(1)
        except Exception as e:
            print(e)
            print("sleeping for 10sec")
            time.sleep(10)
            main_v2(tt)
        print("sleeping for time interval")
        time.sleep(tt)


if __name__ == "__main__":
    time_interval = 60*60*3  # in seconds
    time_interval_for_tracking = 60*5  # in seconds for 20 people per request
    t1 = threading.Thread(target=main, args=(time_interval,))
    t2 = threading.Thread(target=main_v2, args=(time_interval_for_tracking,))
    t1.start()
    t2.start()
