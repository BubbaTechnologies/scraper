#Matthew Groholski
#Feburary 4th, 2023

import datetime
import os
import re
import random

USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36']

CLOTHING_DICT = {
    "top": "[Tt]ops?|[- ]Shirts?|[Jj]ersey|[Tt]ees?|[Cc]ardigan|[Bb]lazer|[Ff]lannel|[Ss]weater|[Pp]olo|[Vv]est",
    "bottom": "[Jj]eans?|[Ss]horts?|[Pp]ants?|[Tt]rousers|[Jj]oggers|[Ll]eggings|[Ss]lacks",
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
        'User-Agent': random.choice(USER_AGENTS)
    }

    return headers

def cleanString(string: str):
    string = string.strip("\n").replace("\xa0", " ").strip()
    return string

def getGender(string: str):
    string = cleanString(string)
    if re.search("([Me][ae]n)", string):
        return "male"

    if re.search("([Ww]om[ae]n)", string):
        return "female"

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

    p = re.findall(all(), string)

    if len(p) < 1:
        return "other"

    lastString = p[len(p) - 1]

    for i in reDict:
        if re.search(reDict[i], lastString):
            return i

    return "other"