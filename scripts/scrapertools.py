#Matthew Groholski
#August 2nd, 2023

from typing import List

import datetime
import os
import re
import random
import string as stringLibrary
import properties

from typing import Dict

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
    "long sleeve":"(?:^| )([Ff]lannel)|(?:^| )([Tt]urtleneck)|(?:^|\s)([Bb]utton(?:-|\s)[Dd]own)|(?:^| )([Ll]ong [Ss]leeve)|(?:^| )([Ww]affle [Kk]nit)",
    "shirt":"(?:^|[- ])([Ss]hirts?)|(?:^| )(Jersey)|(?:^| )([Tt]ees?)|(?:(^| )([Pp]olo))|(?:^| )([Cc]rew (?:[Nn]eck)?)|(?:^| )([Vv]-[Nn]eck)|(?:^| )([Hh]enley)|(?:^| )[Ss]hort [Ss]leeve",
    "top":"(?:^| )([Tt]ops?(?!coat))|(?:^| )([Cc]ami)|(?:^| )([Cc]orset)|(?:^| )([Bb]odysuit)",
    "sweatshirt":"(?:^| )([Hh]oodie)|(?:^| )([Ss]weatshirt)",
    "tank":"(?:^| )([Tt]anks?(?: [Tt]op)?)",
    "bra":"(?:^| )([Bb]ra(?:lette)?) ",
    "dress":"(?:^| )([Dd]ress)",
    "jacket & vest":"((?:^| )[Cc]ardigan)|(?:^| )([Bb]lazer)|(?:^| )([Ss]weater)|(?:^| )([Vv]est)|(?:^| )([Pp]opover)|(?:^| )([Hh]alf[- ][Zz]ip)|(?:^| )([Ff]leece)"\
        "|(?:^| )([Jj]acket)|(?:^| )([Hh]oodie)|(?:^| )([Pp]ullover)|"\
        "(?:^| )([Ss]hacket)|(?:^| )([Aa]norak)|(?:^| )([Pp]arka)|(?:^| )([Bb]omber)|(?:^| )([Cc]oat)|(?:^| )([Ss]weatshirt)|(?:^| )([Aa]norak)|(?:^| )([Ww]ind [Bb]reaker)",
    "shorts":"(?:^| )\b([Ss]horts?)(?! [Ss]leeve)\b",
    "jeans":"(?:^| )([Jj]eans?)",
    "leggings":"(?:^| )([Ll]eggings?)",
    "romper & jumper":"(?:^| )([Jj]umper)|(?:^| )([Oo]nesie)|(?:^| )([Pp]laysuit)|(?:^| )([Rr]omper)|(?:^| )([Jj]umpsuit)",
    "skirt":"(?:^| )([Ss]kirt)|(?:^| )([Ss]kort)",
    "pants":"(?:^| )([Pp]ants?)|(?:^| )([Tt]rousers?)|(?:^| )([Jj]oggers?)|(?:^| )([Ss]lacks)|(?:^| )([Cc]hinos?)|(?:^| )([Hh]igh[- ][Rr]ise)|(?:^| )([Ss]weatpants?)",
    "set":"(?:^| )([S|s]ets?)",
    "sleepwear":"(?:^| )([Ss]leepwear)|(?:^| )([Pp]ajamas?)|(?:^| )([Nn]ightie)|(?:^| )([Rr]obe)",
    "swimwear":"(?:^| )([Ss]wim)|(?:^| )([Bb]ikini)|(?:^| )([Rr]ash(?: )?[Gg]uard)|(?:^| )([Ss]urf(?![- ]?[Bb]oard))|(?:^| )([Tt]runk[s]?)|(?:^| )([Ww]et(?:[Ss]uit)?)|(?:^| )([Oo]ne[- ][Pp]iece)",
    "shoes":"(?:^| )([Ss]hoes?)|(?:^| )([Ss]andals?)|(?:^| )([Ss]lides)|(?:^| )([Bb]oots?)|(?:^| )([Ss]neakers?)|(?:^| )([Hh]eels?)|(?:^| )([Ss]tilettos?)|(?:^| )([Ff]latforms?)|(?:^| )([Ww]edges?)|(?:^| )([Pp]umps?)",
    "suit & tuxedo":"(?:^| )([Ss]uit)|(?:^| )([Tt]uxedo)",
    "underclothing":"(?:^| )([Uu]nderwear)|(?:^| )([Bb]oxers?)|(?:^| )([Bb]riefs?)|(?:^| )([Tt]hong)|(?:^| )([Pp]ant(?:ies|y))|(?:^| )([Gg]arter)|(?:^| )([Bb]abydoll)|(?:^| )([Tt]edd(?:ies|y(?! ?[Bb]ear)))",
    "accessories":"(?:^| )([Tt]ights)|(?:^| )([Ss]tockings)|(?:^| )([Tt]high(?: )?[Hh]ighs?)|(?:^| )([Bb]ackpack)|(?:^| )([Pp]urse)|(?:^| )([Bb]ag)|(?:^| )([Bb]elt)|(?:^| )(" \
                 "[Pp]erfume)|(?:^| )([Cc]ologne)|(?:^| )([Hh]at)|(?:^| )([Gg]lasses)|(?:^| )([Ww]atch)|(?:^| )([Nn]ecklace)|(?:^| )([Ww]allet)|(?:^| )([Pp]in)|(?:^| )([Cc]uff(?:s|links))|" \
                 "(?:^| )([Pp]ocket [Ss]quares)|(?:^| )([Cc]lip)|(?:^| )([Rr]ing)|(?:^| )([Ee]arings)|(?:^| )([Pp]endant)|(?:^| )([Bb]raclet)|(?:^| )([Bb]rooches?)|(?:^| )([Bb]ands?)|" \
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
"""
    Parameters:
        - string: A string that will be used to determine the gender.
    Return:
        - A string with the determined gender.
"""
def getGender(string: str)->str:
    string = cleanString(string).lower()

    if re.search("(?:^| )([Ww]om[ae]n)|([Ff]emale)(?:$| )", string):
        return "female"

    if re.search("(?:^| )([Mm][ae]n)|([Mm]ale)(?:$| )", string):
        return "male"

    if re.search("(?:^| )([Gg])irl(?:$| )", string):
        return "girl"

    if re.search("(?:^| )([Bb])oy(?:$| )", string):
        return "boy"

    if re.search("(?:^| )([Kk]id)(?:$| )", string):
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

def getTags(strings: List[str], customRegex: Dict[str,List[str]] = None)->List[str]:
    for i in range(len(strings)):
        strings.insert(i, cleanString(strings.pop(i)).lower())

    regexDict = TAG_DICT
    if customRegex:
        regexDict = customRegex

    tags = set()
    for string in strings:
        for p in re.finditer(getTagRegex(regexDict), string):
            for i in regexDict:
                if re.search(regexDict[i], p.group()):
                    tags.add(i)
    return list(tags)

def removeDescriptors(string: str)->str:
    #Removes any parenthesis
    parentheisMatch = re.search("\(.+\)", string)
    if parentheisMatch:
        string = string[:parentheisMatch.start()] + string[parentheisMatch.end():]

    #TODO: Beginning Descriptors
    descriptorMatch = re.search("( - | \| |\*).+", string)
    if descriptorMatch:
        string = string[:descriptorMatch.start()] + string[descriptorMatch.end():]

    return stringLibrary.capwords(string, " ")

def getCatalogApiUrl(url: str, regexList: List[str], urlEncoding: str):
    try:
        for i in re.finditer("{regex\[([0-9]+)\]\[([0-9]+)\]}", urlEncoding):
            replacement = re.search(regexList[int(i.group(1))], url).group(int(i.group(2)))
            urlEncoding = urlEncoding[:i.start()] + replacement + urlEncoding[i.end():]
        return urlEncoding
    except Exception as e:
        printMessage("Invalid catalog API url encoding. Exception: " + str(e))

def getProductApiUrl(baseUrl: str, productUrl: str, apiUrl: str) -> str:
    #Removes base url from productUrl
    route = productUrl[len(baseUrl):]
    parameters = re.search(r"\?.+$", route)
    if parameters:
        route = route[:len(route) - len(parameters.group())]
        parameters = parameters.group(0)

    baseMatch = re.search("{baseUrl}", apiUrl)
    if baseMatch:
        apiUrl = apiUrl[:baseMatch.start()] + baseUrl + apiUrl[baseMatch.end():]

    routeMatch = re.search("{route}", apiUrl)
    if routeMatch:
        apiUrl = apiUrl[:routeMatch.start()] + route + apiUrl[routeMatch.end():]

    parametersMatch = re.search("{parameters}", apiUrl)
    if parametersMatch and parameters:
        apiUrl = apiUrl[:parametersMatch.start()] + parameters + apiUrl[parametersMatch.end():]
    elif parametersMatch and not parameters:
        apiUrl = apiUrl[:parametersMatch.start()] + apiUrl[parametersMatch.end():]

    return apiUrl

def cleanUrl(url: str):
    urlRe = re.match("[^#]+", url)
    if urlRe:
        return urlRe.group(0)
    return url

#Returns the product url information for Catalog API. 
#Returns a tuple of strings with the following format: (productUrl, jsonRoute)
def getProductUrlInformation(encoding: str)->tuple[str, str]:
    #Gets jsonRoute; defaults variable to entire encoding
    jsonRoute = encoding
    productUrl = ""
    jsonRouteSearch = re.search("{(.+?)}", encoding)
    if jsonRouteSearch:
        jsonRoute = encoding[jsonRouteSearch.start(1):jsonRouteSearch.end(1)]
        productUrl = encoding[:jsonRouteSearch.start()] + '{data}' + encoding[jsonRouteSearch.end():]
    return (productUrl, jsonRoute)

#Creates Url
#Searches for {data} and inserts data as replacement
def buildUrl(urlEncoding: str, data: str)->str:
    return urlEncoding.replace("{data}", data)

#Creates jsonRoute with parameters
def getJsonRoute(route: str, urlParameters:Dict[str, str])->str:
    for i in re.finditer("(?:{param:)(.+?)(?:})", route):
        try:
            route = route[:i.start()] + urlParameters[i.group(1)] + route[i.end():]
        except:
            openingPosition = 0
            closingPosition = i.end()

            #Finds first [ before closingPosition
            for j in range(closingPosition, 0, -1):
                if route[j] == '[':
                    openingPosition = j + 1
                    break

            route = route[:openingPosition] + "0" + route[closingPosition:]
            printMessage("No URL parameter \"{0}\" replacing with index zero.".format(i.group(1)))

    return route.split("/")

#Parses Json Structure
def parseJson(routeList: List[str], jsonObj)->List:
    #NOTE: Avoids circular import
    from classes import Relation

    if len(routeList) == 0:
        return jsonObj
    
    currentRoute: str = routeList[0]
    returnList = []
    #Checks for condition
    condition: re.Match = re.search("\[(.+)(=|!=|<=|<|>|>=)(.+)\]", currentRoute)
    if condition:
        try:
            operator = Relation(condition.group(2))
            key, value = (condition.group(1), condition.group(3))
            currentRoute = currentRoute[:condition.start()]
            for i in jsonObj[currentRoute]:
                if operator.compute(str(i[key]), str(value)):
                    data = parseJson(routeList[1:], i)
                    if type(data) == list:
                        returnList += data
                    else:
                        returnList.append(data)
        except:
            printMessage("Invalid JSON route: {0}".format(currentRoute))
            exit()

    #Checks for number index
    index: re.Match = re.search("(?:\[)([0-9]+)(?:\])", currentRoute)
    if index:
        currentRoute = currentRoute[:index.start()]  
        index = int(index.group(1))
        data = parseJson(routeList[1:], jsonObj[currentRoute][index])
        if type(data) == list:
            returnList += data
        else:
            returnList.append(data)
        return returnList


    #Checks for all operator
    operator: re.Match = re.search("\[(\*)\]", currentRoute)
    if operator:
        for i in jsonObj[currentRoute[:operator.start()]]:
            data = parseJson(routeList[1:], i)
            if type(data) == list:
                returnList += data
            else:
                returnList.append(data)
        return returnList
        
    #No condition
    data = parseJson(routeList[1:], jsonObj[currentRoute])
    if type(data) == list:
        returnList = data
    else:
        returnList.append(data)

    return returnList

#Misc
def printMessage(message: str) -> None:
    print(datetime.datetime.now().strftime("%H:%M:%S") + ": " + message)

def cleanString(string: str):
    strings = string.strip().strip("\n").split("\n")
    for i in range(len(strings)):
        newString = strings[i].strip("\n").replace("\xa0", " ").strip()
        #Removes any HTML tags
        htmlTagMatch = re.match("<[^/]+>(.+?)<.+>", newString)
        if htmlTagMatch:
            newString = htmlTagMatch.group(1)
        strings[i] = newString
    return (" ".join(strings))

def getCLOTHING_DICT():
    re = ""
    for s in CLOTHING_DICT.values():
        re += s + "|"
    re = re[:-1]
    return re

def getTagRegex(regexDict: Dict):
    re = ""
    for s in regexDict.values():
        re += s + "|"
    re = re[:-1]
    return re

def getUrlParameters(url:str)->Dict:
    params = re.search("(?:\?)(.+)&", url)
    paramDict = {}
    if params:
        params = params.group(1)
        for param in params.split("&"):
            key, value = param.split("=")
            paramDict[key] = value
    return paramDict
