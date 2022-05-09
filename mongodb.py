import requests
import os
import json
from dotenv import load_dotenv
import random
load_dotenv()

# quotes dataset on keggle = https://www.kaggle.com/datasets/akmittal/quotes-dataset

URL = str(os.getenv("MONGO_DB_DATABASE_URL"))

HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': os.getenv("MONGO_DB_API_KEY"),

}


def get_random_quote():
    """Takes nothing
    Returns: dictionary of quote"""
    BODY = {
        "dataSource": "Cluster0",
        "database": "quotes",
        "collection": "quotes",
        "filter": {
            "id": random.randint(1, 48391 + 1)
        }
    }

    try:
        r = requests.post(url=URL+"/action/findOne",
                          headers=HEADERS, json=BODY)
        if r.status_code == 200:
            if json.loads(r.text) == None:
                raise Exception("Nothing recieved: ", r.text)
            else:
                return json.loads(r.text)["document"]
        else:
            raise Exception("Status code: ", r.status_code)

    except Exception as e:
        return e


def get_ID(user=None):
    """takes a user:int or nothing
    If user == None: return dictionary
    else: return tweet id
    returns error
    """
    BODY = {
        "dataSource": "Cluster0",
        "database": "quotes",
        "collection": "ID",
    }

    try:

        r = requests.post(url=URL+"/action/findOne",
                          headers=HEADERS, json=BODY)
        if r.status_code == 200:
            if json.loads(r.text) == None:
                raise Exception("Nothing recieved: ", r.text)
            else:
                if user == None:
                    data = json.loads(r.text)["document"]
                    data.pop("_id")
                    return data
                else:
                    return json.loads(r.text)['document'][str(user)]
        else:
            raise Exception("Status code: ", r.status_code)

    except Exception as e:
        return e


def write_ID(user, tweet_id):
    """takes a user:int and tweet_id:int
    returns error, 0: success, 1: failure"""

    BODY = {
        "dataSource": "Cluster0",
        "database": "quotes",
        "collection": "ID",
        "filter": {
            "_id": {"$oid": "6278ea42071f6d99f360cc8a"}
        },
        "update": {
            "$set": {
                user: {"$numberLong": str(tweet_id)}
            }
        }


    }

    r = requests.post(url=URL+"/action/updateOne",
                      headers=HEADERS, json=BODY)
    if r.status_code == 200:
        if json.loads(r.text) == None:
            raise Exception("Nothing recieved: ", r.text)
        else:
            if json.loads(r.text)['modifiedCount'] != 0:
                return 0
            else:
                raise Exception("MonogDB update error: ", r.content)
    else:
        raise Exception(r.status_code, r.text)


# print(write_ID("1131587879166078977", 654))
# print(get_ID())
# print(get_random_quote())
