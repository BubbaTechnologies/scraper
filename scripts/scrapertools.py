#Matthew Groholski
#Feburary 4th, 2023

import datetime
import os
import re
import random
import requests
from itertools import tee

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
]

REFERER = ["https://www.google.com","https://search.yahoo.com","https://www.bing.com"]

CLOTHING_DICT = {
    "top": "[Tt]ops?|[- ]Shirts?|[Jj]ersey|[Tt]ees?|[Cc]ardigan|[Bb]lazer|[Ff]lannel|[Ss]weater|[Pp]olo|[Vv]est|[Tt]urtleneck|[Hh]enley|[Pp]opover|[Hh]alf[- ][Zz]ip|[Bb]utton[- ]Down|[Cc]rew( [Nn]eck)?|[Tt]ank$|[Vv]-[Nn]eck",
    "bottom": "[Jj]eans?|[Ss]horts?|[Pp]ants?|[Tt]rouser[s]?|[Jj]ogger[s]?|[Ll]egging(s)?|[Ss]lacks|[Cc]hino|[Hh]igh-[Rr]ise",
    "underclothing": "[Uu]nderwear|[Bb]oxer|[Bb]rief[s]?|[Tt]hong|[Pp]ant(?:ies|y)|[Bb]ra(?:lette)?|[Cc]orset|[Gg]arter|[Bb]abydoll|[Tt]edd(?:ies|y)",
    "shoes": "[Ss]hoes?|[Ss]andals|[Ss]lides|[Bb]oots?|[Ss]neakers?|[Hh]eels?|[Ss]tilettos?|[Ff]latforms?|[Ww]edges?|[Pp]umps?",
    "jacket": "[Jj]acket|[Hh]oodie|[Pp]ullover|[Ss]hacket|[Aa]norak|[Pp]arka|[Bb]omber|[Cc]oat|[Ss]weatshirt",
    "sleepwear": "[Ss]leepwear|[Pp]ajamas?|[Nn]ightie|[Rr]obe|[Ss]lip|[Cc]ami(?:sole)?",
    "skirt": "[Ss]kirt|[Ss]kort",
    "one piece": "[Bb]odysuit|[Rr]omper|[Jj]umpsuit|[Oo]ne Piece|[Pp]laysuit",
    "dress":"[Dd]ress",
    "accessory": "[Tt]ights|[Ss]tockings|[Tt]high(?: )?[Hh]ighs?|[Bb]ackpack|[Pp]urse|[Bb]ag|[Bb]elt|" \
                 "[Pp]erfume|[Cc]ologne|[Hh]at|[Gg]lasses|[Ww]atch|[Nn]ecklace|[Ww]allet|[Pp]in|[Cc]uff(?:s|links)" \
                 "[Pp]ocket [Ss]quares|[Cc]lip|[Rr]ing|[Ee]arings|[Pp]endant|[Bb]raclet|[Bb]rooches?|[Bb]ands?|" \
                 "[Ss]carves|[Gg]loves?|[Tt]ies?|[Ss]ocks|[T|t]ote|[Pp]ocket [Ss]quare|[Cc]ap",
    "swimwear": "[Ss]wim|[Bb]ikini|[Rr]ash(?: )?[Gg]uard|[Ss]urf|[Tt]runk[s]?"
}

INVALID_REGEX = "[Gg]ift card"

URL = "https://api.peachsconemarket.com"
JWT = ""

PROXY = {
    "http":f"http://customer-{os.getenv('PROXY_USERNAME')}:{os.getenv('PROXY_PASSWORD')}@us-pr.oxylabs.io:10000",
    "https":f"http://customer-{os.getenv('PROXY_USERNAME')}:{os.getenv('PROXY_PASSWORD')}@us-pr.oxylabs.io:10000"
}
PROXY_ACTIVE=False

def getProxies():
    if PROXY_ACTIVE:
        return PROXY
    else:
        return None

def cdFile(file: str) -> None:
    abspath = os.path.abspath(file)
    directoryName = os.path.dirname(abspath)
    os.chdir(directoryName)

def pwd() -> str:
    return os.getcwd()

def printMessage(message: str) -> None:
    print(datetime.datetime.now().strftime("%H:%M:%S") + ": " + message)

def getHeaders(useReferer=False) -> dict[str, str]:
    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding":"gzip,deflate",
        "Accept-Language":"en-US,en;q=0.9",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "Pragma":"no-cache",
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"none"
        }
    headers["User-Agent"] = random.choice(USER_AGENTS)
    if useReferer:
        headers["Referer"] = random.choice(REFERER)
    return headers

def cleanString(string: str):
    string = string.strip("\n").replace("\xa0", " ").strip()
    return string

def getGender(string: str):
    string = cleanString(string)

    if re.search("([Ww]om[ae]n)|([Ff]emale)", string):
        return "female"

    if re.search("([Mm][ae]n)|([Mm]ale)", string):
        return "male"

    if re.search("([Gg])irl", string):
        return "girl"

    if re.search("([Bb])oy", string):
        return "boy"

    if re.search("([Kk]id)", string):
        return "kids"

    return "other"

def getCLOTHING_DICT():
    re = ""
    for s in CLOTHING_DICT.values():
        re += s + "|"
    re = re[:len(re) - 1]
    return re

def getType(string: str):
    string = cleanString(string)

    reIter = re.finditer(getCLOTHING_DICT(), string)

    if len(tuple(reIter)) > 0:
        *_,p = re.finditer(getCLOTHING_DICT(), string)
        for i in CLOTHING_DICT:
            if re.search(CLOTHING_DICT[i], p.group()):
                return i

    return "other"

class Clothing:
    def __init__(self, name: str, imageUrl: list[str], productUrl: str, storeId: int, type: str, gender: list[str]):
        self.name = name
        self.imageUrl = imageUrl
        self.productUrl = productUrl
        self.storeId = storeId
        self.type = type
        self.gender = gender

    def toDict(self):
        jsonObj = {
            "name": self.name,
            "imageUrl": self.imageUrl,
            "productUrl": self.productUrl,
            "storeId": str(self.storeId),
            "type": self.type,
            "gender": [self.gender]
        }

        return jsonObj

    def toString(self):
        return str(self.toDict())

    def createClothing(self):
        header = {
            "Authorization": "Bearer " + JWT,
            "Content-Type": "application/json"
        }

        r = requests.post(URL + "/scraper/clothing", headers=header, json=self.toDict())
        try:
            return r.json()["id"]
        except KeyError:
            print("Could not create clothing: " + str(r))
            return None
    
    @staticmethod
    def checkClothing(url):
        header = {
            "Authorization": "Bearer " + JWT
        }

        r = requests.get(URL + "/scraper/checkClothing?url=" + url, headers=header)

        if r.status_code == 200 and "{}" not in r.json():
            try:
                if r.json()["id"]:
                    return True
            except KeyError:
                return False
        return False
    
class Store:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.id = -1

    def toDict(self):
        jsonObj = {
            "name": self.name,
            "url": self.url
        }

        return jsonObj

    def toString(self):
        return str(self.toDict())

    def createStore(self):
        headers = {
            "Authorization": "Bearer " + JWT,
            "Content-Type": "application/json"
        }

        r = requests.post(url=URL + "/scraper/store", headers=headers, json=self.toDict())
        try:
            self.id = r.json()["id"]
            return 
        except KeyError:
            print("Could not create store: " + r)
            exit()

#Parses Json Structure
def getJsonRoute(routeList:list, level: int, jsonObj: dict):
    returnList = []

    if len(routeList) - 1 == level:
        return jsonObj[routeList[level]]

    if (routeList[level] == "*"):
        for i in range(len(jsonObj)):
            print(jsonObj[i])
            returnList.append(getJsonRoute(routeList, level + 1, jsonObj[i]))
    else:
        returnList.append(getJsonRoute(routeList, level + 1, jsonObj[routeList[level]]))

    if len(returnList) == 1:
        return returnList[0]
    return returnList