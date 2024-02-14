#Matthew Groholski
#July 22nd, 2023

from bs4 import BeautifulSoup
from typing import List, Dict

import scrapertools
import requests_html, requests, json, asyncio
import re
import time, random
import properties
import classes
import traceback

#Exits program without errors.
async def exitProgram(session: requests_html.AsyncHTMLSession):
    await session.close()
    exit()

#Requests main page.
async def getMainPage(baseUrl: str, session) -> None:
    response = await session.get(baseUrl, headers = scrapertools.getHeaders(useReferer=True))
    scrapertools.printMessage("Received from {0} status code {1}.".format(baseUrl, str(response.status_code)))
    time.sleep(random.randint(properties.SLEEP_FLOOR_SECONDS, properties.SLEEP_CEIL_SECONDS))

#Creates link to store in queue.
async def createLink(route: str, baseUrl: str) -> str:
    baseUrlRegex = baseUrl.replace(".", "\.")
    if not re.search(baseUrlRegex, route):
        return (baseUrl + route)
    return route

#Parse Catalog API for links
async def parseApiForLinks(info: Dict, url: str):
    parameterDict = scrapertools.getUrlParameters(url)
    apiUrl = scrapertools.getCatalogApiUrl(url, info["regex"], info["api"]["urlEncoding"])
    response = requests.get(apiUrl)
    if response.status_code == 200:
        responseAsJson = json.loads(response.text)
        productUrl, jsonRoute = scrapertools.getProductUrlInformation(info["api"]["productUrl"])
        returnList = scrapertools.parseJson(scrapertools.getJsonRoute(jsonRoute, parameterDict), responseAsJson)
        
        for i in range(len(returnList)):
            returnList[i] = scrapertools.cleanUrl(scrapertools.buildUrl(productUrl, returnList[i]))
        return returnList
    raise Exception("Received {0} from {1}.".format(response.status_code, apiUrl))

#Parse API for Clothing
async def parseApiForClothing(info: Dict, url: str, baseUrl: str) -> classes.Clothing:
    parameterDict = scrapertools.getUrlParameters(url)
    apiUrl = scrapertools.getProductApiUrl(baseUrl, url, info["api"]["apiUrlEncoding"])
    response = requests.get(apiUrl)
    if response.status_code == 200:
        responseAsJson = json.loads(response.text)
        name = scrapertools.cleanString(scrapertools.parseJson(scrapertools.getJsonRoute(info["api"]["nameRoute"], parameterDict), responseAsJson)[0])
        imageUrl = scrapertools.parseJson(scrapertools.getJsonRoute(info["api"]["imageRoute"], parameterDict), responseAsJson)
        for i in range(len(imageUrl)):
            if "//" == imageUrl[i][:2]:
                imageUrl[i] = "https://" + imageUrl[i][2:]
        type = scrapertools.getType(name)
        gender = None
        if "gender" in info["api"].keys():
            gender = info["api"]["gender"]
        else:
            tags:List[str] = scrapertools.parseJson(scrapertools.getJsonRoute(info["api"]["genderRoute"], parameterDict), responseAsJson)
            for tag in tags:
                gender = scrapertools.getGender(tag)
                if gender != "other":
                    break
        
        descriptions = scrapertools.parseJson(scrapertools.getJsonRoute(info["api"]["clothingDescription"]["route"], parameterDict), responseAsJson)

        for i in range(len(descriptions)):
            descriptions[i] = scrapertools.cleanString(descriptions[i])

        tags = scrapertools.getTags(descriptions, info["api"]["clothingDescription"]["regex"])

        return classes.Clothing(name, imageUrl, url, type, gender, tags)
    raise Exception("Received {0} from {1}.".format(response.status_code, apiUrl))

#Parse HTML for links.
async def parseHtmlForLinks(regex: List[str], soup: BeautifulSoup)->List[str]:
    results = []
    for a in soup.find_all('a', href = True):
        for ex in regex:
            linkUrl = a["href"]
            if re.search(ex, linkUrl):
                results.append(scrapertools.cleanUrl(linkUrl))
                break
    return results

#Parse html for clothing.
async def parseHtmlForClothing(info: Dict, soup: str, url: str)-> classes.Clothing:
    #Gets product name
    name = scrapertools.cleanString(soup.find("h1", {"class":info["identifiers"]["nameIdentifier"]}).text)
    type = scrapertools.getType(name)

    imageDiv = soup.find("div", {"class": info["identifiers"]["imageDivIdentifier"]})
    imageUrl = []
    for img in imageDiv.find_all("img"):
        if img.has_attr('srcset'):
            imageUrl.append(img['srcset'].split()[0])
        elif img.has_attr('data-originsrc'):
            imageUrl.append(img['data-originsrc'])
        else:
            imageSrc = img['src']
            if re.match("(https://|/)", imageSrc):
                imageUrl.append(imageSrc)

    gender = None
    if "breadcrumbsIdentifier" in info["identifiers"].keys():
        navSearch = soup.find("nav", {"aria-label": info["identifiers"]["breadcrumbsIdentifier"]})
        
        #Attempts to find div
        if not navSearch:
            navSearch = soup.find("div", {"class": info["identifiers"]["breadcrumbsIdentifier"]})
        
        #Attempts to find ordered list
        if not navSearch:
            navSearch = soup.find("ol", {"class": info["identifiers"]["breadcrumbsIdentifier"]})

        #Searchs through links within breadcrumbs
        for link in navSearch.find_all("a"):
            gender = scrapertools.getGender(link.text)
            if gender != "other":
                break
            
            #Checks if url is seperated by gender
            if link.has_attr('href'):
                gender = scrapertools.getGender(link['href'])

                if gender != "other":
                    break
    else:
        gender = info["identifiers"]["gender"]
    gender = scrapertools.getGender(scrapertools.cleanString(gender))

    description = scrapertools.cleanString(soup.find("div",{"class":info["identifiers"]["clothingDescription"]["divIdentifier"]}).text)
    return classes.Clothing(name, imageUrl, url, type, gender, scrapertools.getTags([description]))

async def main():
    #Reads JSON information
    scrapingInfo = {}
    filename = input("")
    with open(filename, "r") as jsonFile:
        scrapingInfo = json.loads(jsonFile.read())

    #Logs into API
    api = classes.Api()

    #Creates store
    store:classes.Store = classes.Store(scrapingInfo["name"], scrapingInfo["url"])
    store.createStore(api.getJwt())

    baseUrl = scrapingInfo["url"]

    #Creates session
    session = requests_html.AsyncHTMLSession()
    catalogQueue = [baseUrl]
    productQueue = []
    indexed = [baseUrl]

    nonAcceptCount = 0

    proxyActive = False
    proxyRequests = 0

    while not (len(catalogQueue)+ len(productQueue)) == 0:
        try:
            #Pops random url within queue
            chance = random.uniform(0,1)
            if (chance >= properties.PRODUCT_PERCENTAGE or len(productQueue) == 0) and len(catalogQueue) > 0:
                url = catalogQueue.pop(0)
            elif len(productQueue) > 0:
                url = productQueue.pop(0)
            else:
                scrapertools.printMessage("No more item or catalog pages.")
                exit(1)

            if proxyRequests > 750:
                await exitProgram(session)
            elif proxyActive:
                proxyRequests += 1

            proxies = scrapertools.getProxies() if proxyActive else None
            headers = scrapertools.getHeaders()
            response = await session.get(url, headers = headers, proxies=proxies)
            if "loadJavascript" in scrapingInfo.keys() and scrapingInfo["loadJavascript"]:
                await response.html.arender(wait = 4, timeout=properties.SCRAPER_TIMEOUT_SECONDS)
            
            if response.status_code != 200:
                scrapertools.printMessage("Received {0} from {1} using {2}.".format(response.status_code, url, headers))

                nonAcceptCount += 1
                if not proxyActive and ('useProxy' in  scrapingInfo.keys()) and scrapingInfo['useProxy']:
                    if len(productQueue) + len(catalogQueue) == 0:
                        #Resets queue
                        catalogQueue = [baseUrl]
                    scrapertools.printMessage("Turning on Proxy.")
                    proxyActive = True
                    nonAcceptCount = 0
                elif nonAcceptCount > 10:
                    await exitProgram(session)
                else:
                    time.sleep(random.randint(properties.SLEEP_FLOOR_SECONDS, properties.SLEEP_CEIL_SECONDS))
                    if random.randint(0,1) == 1:
                        await getMainPage(baseUrl, session)
                continue
            else:
                scrapertools.printMessage("Received {0} from {1}.".format(response.status_code, url))

            soup = BeautifulSoup(response.text, "html.parser")

            catalogResults = []
            productResults = []
            if scrapingInfo["catalogPageInformation"]["api"] and re.search("|".join(scrapingInfo["catalogPageInformation"]["regex"]), url):
                productResults += await parseApiForLinks(scrapingInfo["catalogPageInformation"], url)
            
            catalogResults += await parseHtmlForLinks(scrapingInfo["catalogPageInformation"]["regex"], soup)
            productResults += await parseHtmlForLinks(scrapingInfo["productPageInformation"]["regex"], soup)
            
            for unformattedLink in catalogResults + productResults:
                link = await createLink(unformattedLink, baseUrl)
                if link not in indexed:
                    indexed.append(link)
                    if unformattedLink in catalogResults:
                        scrapertools.printMessage("Appending {0} to catalog queue.".format(link))
                        catalogQueue.append(link)
                    else:
                        scrapertools.printMessage("Appending {0} to product queue.".format(link))
                        productQueue.append(link)
                else:
                    scrapertools.printMessage("Indexed {0} already.".format(link))
            
            #If product url
            if re.search("|".join(scrapingInfo["productPageInformation"]["regex"]), url):
                clothingResult: classes.Clothing = None
                if "api" in scrapingInfo["productPageInformation"].keys():
                    clothingResult = await parseApiForClothing(scrapingInfo["productPageInformation"], url, baseUrl)
                else:
                    clothingResult = await parseHtmlForClothing(scrapingInfo["productPageInformation"], soup, url)
                
                if clothingResult.type == "invalid":
                    scrapertools.printMessage(f"Skipping {url} due to invalid type.")
                    continue

                clothingResult.storeId = store.id
                clothingResult.imageUrl = scrapertools.cleanImageUrls(clothingResult.imageUrl)


                scrapertools.printMessage("Created " + str(clothingResult))
                if clothingResult.createClothing(api.getJwt()):
                    scrapertools.printMessage("Created " + str(clothingResult))

            time.sleep(random.randint(2,10))
            if random.randint(0,1) == 1:           
                await getMainPage(baseUrl, session)
        except Exception as e:
            traceback.print_exc()
            scrapertools.printMessage("Exception: " + str(e))
            pass


if __name__=="__main__":
    asyncio.run(main())