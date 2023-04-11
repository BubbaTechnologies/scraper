#Matthew Groholski
#Feburary 5th, 2023

import scrapertools
import json
import requests_html
import time
import random
from bs4 import BeautifulSoup
import re
import asyncio
import requests
import os

async def main():
    #Connect to api

    data = {
        "username": os.getenv("PEACHSCONE_API_USERNAME"),
        "password": os.getenv("PEACHSCONE_API_PASSWORD")
    }

    response = requests.post("https://api.peachsconemarket.com/login", headers={"Content-Type":"application/json"}, json = data)
    scrapertools.JWT = json.loads(response.text)["jwt"]


    #Opens file
    filename = input()
    jsonFile = open(filename, "r")
    
    info = json.loads(jsonFile.read())

    store:scrapertools.Store = scrapertools.Store(info["name"], info["url"])
    store.createStore()

    basicUrl = info["url"]
    queue = ["https://bonobos.com/products/herringbone-5-pocket-pants?color=naval%20blue", basicUrl]

    session = requests_html.AsyncHTMLSession()
    indexed = []
    nonAcceptCount = 0

    while not len(queue) == 0:
        time.sleep(random.randint(2,7))
        url = queue.pop(0)
        indexed.append(url)

        response = await session.get(url, headers = scrapertools.getHeaders())
        response.html.arender()
        scrapertools.printMessage("Received from " + url + " status code " + str(response.status_code))

        if not response.status_code == 200:
            nonAcceptCount += 1
            if nonAcceptCount > 10:
                exit()
            else:
                continue
            
        #Resets nonAcceptCount when accepted
        nonAcceptCount = 0

        #Filters through links
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all('a', href = True):
            for regex in info["webpageRegex"] + info["clothingRegex"]:
                search = re.search(regex, a["href"])
                if search is not None and search.group(0) not in indexed and not scrapertools.Clothing.checkClothing(a["href"]):
                    urlString = search.group(0)
                    indexed.append(urlString)

                    #Checks for basicUrl
                    basicUrlRegex = basicUrl.replace(".", "\.")
                    search = re.search(basicUrlRegex, urlString)
                    if search == None:
                        urlString = basicUrl + urlString
                    
                    scrapertools.printMessage(f"Appending {urlString} to queue.")
                    queue.append(urlString)
                    break

        #Checks if current page is clothing
        for regex in info["clothingRegex"]:
            search = re.search(regex, url)
            print(url, regex, str(search is not None))
            if search is not None:
                try:
                    #Gets name
                    name = soup.find("h1", {"class":info["nameIdentifier"]}).text
                    #Get all images
                    imageDiv = soup.find("div", {"class": info["imageIdentifier"]})
                    imageSrc = []
                    for img in imageDiv.find_all("img"):
                        imageSrc.append(img['src'])
                    if "breadcrumbsIdentifier" in info.keys():
                        search = soup.find("nav", {"aria-label": info["breadcrumbsIdentifier"]})
                        if search == None:
                            search = soup.find("div", {"class": info["breadcrumbsIdentifier"]})
                        for link in search.find_all("a"):
                            gender = scrapertools.getGender(link.text)
                            if gender != "other":
                                break
                    elif "gender" in info.keys():
                        gender = scrapertools.getGender(info["gender"])
                    else:
                        gender = "other"
                    clothingType = scrapertools.getType(name)
                    clothing = scrapertools.Clothing(name, imageSrc, url, store.id, clothingType, gender)
                    clothing.createClothing()
                    scrapertools.printMessage("Created " + clothing.toString())
                except Exception as e:
                    scrapertools.printMessage(f"Exception occured while scraping {url}: {str(e)}")
                    break
                

if __name__ == "__main__":
    asyncio.run(main())