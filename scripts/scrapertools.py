#Matthew Groholski
#August 2nd, 2023

from typing import List

import datetime
import os
import re2 as re
import random
import string as stringLibrary
import properties

from typing import Dict
from classes import Relation

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
    "shirt":"(?:^|[- ])([Ss]hirts?)|(?:^| )(Jersey)|(?:^| )([Tt]ees?)|(?:(^| )([Pp]olo))|(?:^| )([Cc]rew (?:[Nn]eck)?)|(?:^| )([Vv]-[Nn]eck)",
    "top":"(?:^| )([Tt]ops?)|(?:^| )([Cc]ami)|(?:^| )([Cc]orset)|(?:^| )([Bb]odysuit)",
    "long sleeve":"(?:^| )([Ff]lannel)|(?:^| )([Tt]urtleneck)|(?:^| )([Hh]enley)|(?:^|\s)([Bb]utton(?:-|\s)[Dd]own)|(?^| )([Ll]ong [Ss]leeve)|(?:^| )([Ww]affle [Kk]nit)",
    "sweatshirt":"(?:^| )([Hh]oodie)|(?:^| )([Ss]weatshirt)",
    "tanks":"(?:^| )([Tt]anks? (?:[Tt]op))",
    "bras":"(?:^| )([Bb]ra(?:lette)?)",
    "dresses":"(?:^| )([Dd]ress)",
    "jackets & vests":"((?:^| )[Cc]ardigan)|(?:^| )([Bb]lazer)|(?:^| )([Ss]weater)|(?:^| )([Vv]est)|(?:^| )([Pp]opover)|(?:^| )([Hh]alf[- ][Zz]ip)|(?:^| )([Ff]leece)"\
        "|(?:^| )([Jj]acket)|(?:^| )([Hh]oodie)|(?:^| )([Pp]ullover)|"\
        "(?:^| )([Ss]hacket)|(?:^| )([Aa]norak)|(?:^| )([Pp]arka)|(?:^| )([Bb]omber)|(?:^| )([Cc]oat)|(?:^| )([Ss]weatshirt)|(?:^| )([Aa]norak)",
    "shorts":"(?:^| )([Ss]horts?)",
    "jeans":"(?:^| )([Jj]eans)",
    "leggings":"(?:^| )([Ll]eggings?)",
    "rompers & jumpers":"(?:^| )([Jj]umper)|(?:^| )([Oo]nesie)|(?:^| )([Pp]laysuit)|(?:^| )([Rr]omper)|(?:^| )([Jj]umpsuit)",
    "skirt":"(?:^| )([Ss]kirt)|(?:^| )([Ss]kort)",
    "pants":"(?:^| )([Pp]ants?)|(?:^| )([Tt]rousers?)|(?:^| )([Jj]oggers?)|(?:^| )([Ss]lacks)|(?:^| )([Cc]hinos?)|(?:^| )([Hh]igh[- ][Rr]ise)|(?:^| )([Ss]weatpants?)",
    "sets":"(?:^| )([S|s]ets?)",
    "sleepwear":"(?:^| )([Ss]leepwear)|(?:^| )([Pp]ajamas?)|(?:^| )([Nn]ightie)|(?:^| )([Rr]obe)",
    "swimwear":"(?:^| )([Ss]wim)|(?:^| )([Bb]ikini)|(?:^| )([Rr]ash(?: )?[Gg]uard)|(?:^| )([Ss]urf(?![- ]?[Bb]oard))|(?:^| )([Tt]runk[s]?)|(?:^| )([Ww]et(?:[Ss]uit)?)|(?:^| )([Oo]ne[- ][Pp]iece)",
    "shoes":"(?:^| )([Ss]hoes?)|(?:^| )([Ss]andals)|(?:^| )([Ss]lides)|(?:^| )([Bb]oots?)|(?:^| )([Ss]neakers?)|(?:^| )([Hh]eels?)|(?:^| )([Ss]tilettos?)|(?:^| )([Ff]latforms?)|(?:^| )([Ww]edges?)|(?:^| )([Pp]umps?)",
    "suits & tuxedos":"(?:^| )([Ss]uit)|(?:^| )([Tt]uxedo)",
    "underclothing":"(?:^| )([Uu]nderwear)|(?:^| )([Bb]oxers?)|(?:^| )([Bb]riefs?)|(?:^| )([Tt]hong)|(?:^| )([Pp]ant(?:ies|y))|(?:^| )([Gg]arter)|(?:^| )([Bb]abydoll)|(?:^| )([Tt]edd(?:ies|y(?! ?[Bb]ear)))",
    "accessories":"(?:^| )([Tt]ights)|(?:^| )([Ss]tockings)|(?:^| )([Tt]high(?: )?[Hh]ighs?)|(?:^| )([Bb]ackpack)|(?:^| )([Pp]urse)|(?:^| )([Bb]ag)|(?:^| )([Bb]elt)|(?:^| )(" \
                 "[Pp]erfume)|(?:^| )([Cc]ologne)|(?:^| )([Hh]at)|(?:^| )([Gg]lasses)|(?:^| )([Ww]atch)|(?:^| )([Nn]ecklace)|(?:^| )([Ww]allet)|(?:^| )([Pp]in)|(?:^| )([Cc]uff(?:s|links))|" \
                 "[Pp]ocket [Ss]quares)|(?:^| )([Cc]lip|(?:^| )([Rr]ing|(?:^| )([Ee]arings|(?:^| )([Pp]endant|(?:^| )([Bb]raclet|(?:^| )([Bb]rooches?|(?:^| )([Bb]ands?|(?:^| )(" \
                 "(?:^| )([Ss]carves)|(?:^| )([Gg]loves?)|(?:^| )([Tt]ies?)|(?:^| )([Ss]ocks)|(?:^| )([T|t]ote)|(?:^| )([Pp]ocket [Ss]quare)|(?:^| )([Cc]ap)|(?:^| )([Cc]hoker)|(?:^| )([Bb]eanie)"
}

TAG_DICT = {
    "active": "([Ww]orking out)|([Tt]raining)|([Pp]ractice)|([Ss]port)|([Ww]orkouts?)|([Ss]weat(?!pants?))|([Rr]un(?:ning)?)"
}

INVALID_REGEX = "[Gg]ift [Cc]ard"

# File Builder Tools
def cdFile(file: str) -> None:
    abspath = os.path.abspath(file)
    directoryName = os.path.dirname(abspath)
    os.chdir(directoryName)

def pwd() -> str:
    return os.getcwd()

#Networking tools
def getProxies():
    return properties.PROXY

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

#Data Scraping
def getGender(string: str):
    string = cleanString(string).lower()

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

def getType(string: str):
    string = cleanString(string).lower()

    if re.search(INVALID_REGEX, string):
        return "invalid"
    
    listString = string.split(" ")
    listString.reverse()
    for p in re.finditer(getCLOTHING_DICT(), ' '.join(listString)):
        for i in CLOTHING_DICT:
            if re.search(CLOTHING_DICT[i], p.group()):
                return i

    return "other"

#TODO: Beginning descriptors
def removeDescriptors(string: str)->str:
    #Removes any parenthesis
    parentheisMatch = re.search("\(.+\)", string)
    if parentheisMatch:
        string = string[:parentheisMatch.start()] + string[parentheisMatch.end():]

    descriptorMatch = re.search("( - | \| |\*).+", string)
    if descriptorMatch:
        string = string[:descriptorMatch.start()] + string[descriptorMatch.end():]

    return stringLibrary.capwords(string, " ")

def getApiUrl(baseUrl: str, productUrl: str, apiUrl: str) -> str:
    #Removes base url from productUrl
    route = productUrl[len(baseUrl):]
    parameters = re.search(r"\?.+$", route)
    if parameters:
        route = route[:len(route) - len(parameters.group())]
        parameters = parameters.group(0)

    baseMatch = re.search("{baseUrl}", apiUrl)
    if baseMatch:
        apiUrl = apiUrl[:baseMatch.start()] + baseUrl + apiUrl[baseMatch.end():]
    else:
        printMessage("JSON Error! No {baseUrl} in apiUrlEncoding.")
        exit()

    routeMatch = re.search("{route}", apiUrl)
    if routeMatch:
        apiUrl = apiUrl[:routeMatch.start()] + route + apiUrl[routeMatch.end():]
    else:
        printMessage("JSON Error! No {route} in apiUrlEncoding.")
        exit()

    parametersMatch = re.search("{parameters}", apiUrl)
    if parametersMatch:
        apiUrl = apiUrl[:parametersMatch.start()] + parameters + apiUrl[parametersMatch.end():]

    return apiUrl

def getJsonRoute(route: str, urlParameters:Dict[str, str])->str:
    for i in re.finditer("(?:{param:)(.+?)(?:})", route):
        try:
            route = route[:i.start()] + urlParameters[i.group(1)] + route[i.end():]
        except:
            printMessage("No URL parameter {0}.".format(i.group(1)))
    return route

#Parses Json Structure
def parseJson(routeList: List[str], jsonObj):
    if len(routeList) == 0:
        return jsonObj
    
    currentRoute: str = routeList.pop(0)

    #Checks for condition
    conditionSearch: re.Match = re.search("\[.+\]", currentRoute)
    if conditionSearch:
        condition = currentRoute[conditionSearch.start()+1:conditionSearch.end()-1]
        try:
            operator = Relation(re.search("(>=|>|=|!=|<|<=)",condition).group(1))
            key, value = condition.strip().split(operator.value)
            currentRoute = currentRoute[:conditionSearch.start()]
            for i in jsonObj[currentRoute]:
                if operator.compute(str(i[key]), str(value)):
                    return parseJson(routeList, i)
        except:
            printMessage("Invalid JSON route: {0}".format(currentRoute))
            exit()
            
    #No condition
    return parseJson(routeList, jsonObj[currentRoute])

#Misc
def printMessage(message: str) -> None:
    print(datetime.datetime.now().strftime("%H:%M:%S") + ": " + message)

def cleanString(string: str):
    string = string.strip("\n").replace("\xa0", " ").strip()
    return string

def getCLOTHING_DICT():
    re = ""
    for s in CLOTHING_DICT.values():
        re += s + "|"
    re = re[:len(re) - 1]
    return re