#Matthew Groholski
#Feburary 4th, 2023

import datetime
import os
import re
import random
import requests



USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Avast/111.0.20716.147",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"]

CLOTHING_DICT = {
    "top": "[Tt]ops?|[- ]Shirts?|[Jj]ersey|[Tt]ees?|[Cc]ardigan|[Bb]lazer|[Ff]lannel|[Ss]weater|[Pp]olo|[Vv]est",
    "bottom": "[Jj]eans?|[Ss]horts?|[Pp]ants?|[Tt]rousers|[Jj]oggers|[Ll]eggings|[Ss]lacks|[Cc]hino",
    "underclothing": "[Uu]nderwear|[Bb]oxer|[Bb]rief[s]*|[Tt]hong|[Pp]ant(?:ies|y)|[Bb]ra(?:lette)?|[Cc]orset|[Gg]arter|[Bb]abydoll|[Tt]edd(?:ies|y)",
    "shoes": "[Ss]hoes?|[Ss]andals|[Ss]lides|[Bb]oots?|[Ss]neakers?|[Hh]eels?|[Ss]tilettos?|[Ff]latforms?|[Ww]edges?|[Pp]umps?",
    "jacket": "[Jj]acket|[Hh]oodie|[Pp]ullover",
    "sleepwear": "[Ss]leepwear|[Pp]ajamas?|[Nn]ightie|[Rr]obe|[Ss]lip|[Cc]ami(?:sole)?",
    "skirt": "[Ss]kirt|[Ss]kort",
    "one piece": "[Bb]odysuit|[Rr]omper|[Dd]ress|[Jj]umpsuit",
    "accessory": "[Tt]ights|[Ss]tockings|[Tt]high(?: )?[Hh]ighs?|[Bb]ackpack|[Pp]urse|[Bb]ag|[Bb]elt|" \
                 "[Pp]erfume|[Cc]ologne|[Hh]at|[Gg]lasses|[Ww]atch|[Nn]ecklace|[Ww]allet|[Pp]in|[Cc]uff(?:s|links)" \
                 "[Pp]ocket [Ss]quares|[Cc]lip|[Rr]ing|[Ee]arings|[Pp]endant|[Bb]raclet|[Bb]rooches?|[Bb]ands?|" \
                 "[Ss]carves|[Gg]loves?|[Tt]ies?|[Ss]ocks|[T|t]ote",
    "swimwear": "[Ss]wim|[Bb]ikini|[Rr]ash(?: )?[Gg]uard|[Ss]urf"
}

URL = "https://api.peachsconemarket.com"
JWT = ""

def cdFile(file: str) -> None:
    abspath = os.path.abspath(file)
    directoryName = os.path.dirname(abspath)
    os.chdir(directoryName)

def pwd() -> str:
    return os.getcwd()

def printMessage(message: str) -> None:
    print(datetime.datetime.now().strftime("%H:%M:%S") + ": " + message)

def getHeaders() -> dict[str, str]:
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Connection': 'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests':'1'
    }
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

    p = re.findall(getCLOTHING_DICT(), string)

    if len(p) < 1:
        return "other"

    lastString = p[len(p) - 1]

    for i in CLOTHING_DICT:
        if re.search(CLOTHING_DICT[i], lastString):
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
            "gender": self.gender
        }

        return jsonObj

    def toString(self):
        return str(self.toDict())

    def createClothing(self):
        item = self.checkClothing(self.productUrl)
        if item is not None:
            return item

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