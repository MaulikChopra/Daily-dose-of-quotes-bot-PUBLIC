import requests
import json

"""Documentation: https://github.com/lukePeavey/quotable
"""


class __QuoteStructure:
    """
    Returns everything as string
    content = returns content
    author = returns author
    authorSulg = returns authorSlug
    id = returns id
    length = returns length
    tags = return tags
    pointer = returns http pointer
    request send and check helper function.
    """

    def __init__(self):
        self.URL = 'https://api.quotable.io/random'

    def content(self):
        return self.raw_quote["content"]

    def author(self):
        return self.raw_quote["author"]

    def authorSlug(self):
        return self.raw_quote["authorSlug"]

    def id(self):
        return self.raw_quote["_id"]

    def length(self):
        return self.raw_quote["length"]

    def tags(self):
        return self.raw_quote["tags"]

    def pointer(self):
        return self.pointerobject

    def _sendRequestAndCheck(self, load=None):
        if load == None:  # for the Random() method without load.
            pp = requests.get(self.URL)
        else:  # fetch with the load argument.
            pp = requests.get(self.URL, load)
        # check for status codes.
        if pp.status_code == 200:
            return pp  # all fine
        elif pp.status_code == 404:
            raise Exception("Invalid input or quote not found")
        else:
            raise Exception("Side Down")


class Random(__QuoteStructure):
    """
    Gets a Random quote from https://api.quotable.io/random
    """

    def __init__(self):
        self.URL = 'https://api.quotable.io/random'
        self.fetchedURL = None
        self.raw_quote = json.loads(self.__helper())

    def __helper(self):
        raw_data = self._sendRequestAndCheck()
        self.fetchedURL = raw_data.url
        return raw_data.text


class RandomTag(__QuoteStructure):
    """
    Gets a random quote using tags and function.
    Tag-> List of strings 
    Function-> "and", "or"
    Note: Give a one string list for single Tag
    """

    def __init__(self, tagslist, function=None):
        self.URL = 'https://api.quotable.io/random'
        self.raw_quote = ''
        self.pointerobject = None
        if len(tagslist) == 1 and function == None:
            self.raw_quote = self.__helperSINGLE(tagslist[0])
        elif len(tagslist) != 1 and function == "and":
            self.raw_quote = self.__helperAND(tagslist)
        elif len(tagslist) != 1 and function == "or":
            self.raw_quote = self.__helperOR(tagslist)
        else:
            raise Exception("Invalid Input Arguments")

    def __helperAND(self, tagslist):
        strformat = ",".join(tagslist)
        payload = {"tags": strformat}
        raw = self._sendRequestAndCheck(payload)
        self.pointerobject = raw
        return json.loads(raw.text)

    def __helperOR(self, tagslist):
        strformat = "|".join(tagslist)
        payload = {"tags": strformat}
        raw = self._sendRequestAndCheck(payload)
        self.pointerobject = raw
        return json.loads(raw.text)

    def __helperSINGLE(self, singletag):
        payload = {"tags": singletag}
        raw = self._sendRequestAndCheck(payload)
        self.pointerobject = raw
        return json.loads(raw.text)


class RandomLen(__QuoteStructure):
    """
    Gets a random quote using length(int)
    minlength, maxlength
    """

    def __init__(self, minlength=None, maxlength=None):
        self.URL = 'https://api.quotable.io/random'
        self.raw_quote = ''
        self.pointerobject = None
        if maxlength == None and minlength == None:
            raise Exception(
                "No length specified. Please spepecify minlength or maxlength")
        else:
            self.raw_quote = self.__helper(minlength, maxlength)

    def __helper(self, min, max):
        payload = {"minLength": min, "maxLength": max}
        raw = self._sendRequestAndCheck(payload)
        self.pointerobject = raw
        return json.loads(raw.text)


if __name__ == "__main__":
    r = RandomLen(50, 100)
    print(r.pointer().url)
    print(r.content())
