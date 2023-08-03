#Matthew Groholski
#July 22nd, 2023

from bs4 import BeautifulSoup
from typing import List, Dict, Union

import scrapertools
import requests_html, requests, json, asyncio
import re
import time, random, os, sys
import io, datetime
import properties
import classes
import traceback

async def exitProgram(session: requests_html.AsyncHTMLSession):
    await session.close()
    exit()

async def getMainPage(baseUrl: str, session) -> None:
    response = await session.get(baseUrl, headers = scrapertools.getHeaders(useReferer=True))
    scrapertools.printMessage("Recieved from {0} status code {1}.".format(baseUrl, str(response.status_code)))
    time.sleep(random.randint(properties.SLEEP_FLOOR_SECONDS, properties.SLEEP_CEIL_SECONDS))

async def processHtmlForLinks(soup: BeautifulSoup, queue: List[str], indexed:List[str], info: Dict[str,Union[str, List[str]]]):
    for a in soup.find_all('a', href = True):
        for regex in info["webpageRegex"] + info["clothingRegex"]:
            linkUrl = a["href"]
            if re.search(regex, linkUrl):
                url = re.search("^([^&]*)", linkUrl).group(1)
                url = (info["url"] + url) if not re.search(info["url"].replace(".","\."), url) else url

                if url not in indexed:
                    indexed.append(url)
                    scrapertools.printMessage("Append {0} to queue.".format(url))
                    queue.append(url)
                    break

async def processApiResponse():
    pass

async def processHtmlResponse():
    pass

async def main():
    #Logs into API
    api = classes.Api()

    #Reads JSON information
    scrapingInfo = {}
    filename = input("Filename: ")
    with open(filename, "r") as jsonFile:
        scrapingInfo = json.loads(jsonFile.read())

    #Creates store
    store:classes.Store = classes.Store(scrapingInfo["name"], scrapingInfo["url"])
    store.createStore(api.getJwt())

    baseUrl = scrapingInfo["url"]

    #Creates session
    session = requests_html.AsyncHTMLSession()
    queue = [baseUrl]
    indexed = [baseUrl]

    nonAcceptCount = 0

    proxyActive = False
    proxyRequests = 0

    while not len(queue) == 0:
        try:
            #Pops random url within queue
            url = queue.pop(random.randrange(len(queue)))

            if proxyRequests > 750:
                await exitProgram(session)
            elif proxyActive:
                proxyRequests += 1

            proxies = scrapertools.getProxies() if proxyActive else None
            headers = scrapertools.getHeaders()
            response = await session.get(url, headers = headers, proxies=proxies)
            await response.html.arender(wait = 4, timeout=properties.SCRAPER_TIMEOUT_SECONDS)

            if response.status_code != 200:
                scrapertools.printMessage("Recieved {0} from {1} using {2}.".format(response.status_code, url, headers))

                nonAcceptCount += 1
                if not proxyActive:
                    if len(queue) == 0:
                        #Resets queue
                        queue = [baseUrl]
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
                scrapertools.printMessage("Recieved {0} from {1}.".format(response.status_code, url))

            nonAcceptCount = 0
            soup = BeautifulSoup(response.text, "html.parser")
            await processHtmlForLinks(soup, queue, indexed, scrapingInfo)

            #TODO: Parse API
            #TODO: Parse HTML page
        except Exception as e:
            traceback.print_exc()
            print(e)
            pass


if __name__=="__main__":
    asyncio.run(main())