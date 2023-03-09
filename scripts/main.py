#Matthew Groholski
#Feburary 5th, 2023

import scrapertools
import json
import requests_html
import time
import random
from bs4 import BeautifulSoup
import re

async def main():
    #TODO: Connect to database

    #Opens file
    filename = input()
    jsonFile = open(filename, "r")
    
    info = json.loads(jsonFile.read())

    basicUrl = info["url"]
    queue = [basicUrl]

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
                if search is not None and search.group(0) not in indexed:
                    urlString = search.group(0)
                    indexed.append(urlString)

                    #Checks for basicUrl
                    basicUrlRegex = basicUrl.replace(".", "\.")
                    if not basicUrlRegex.search(search):
                        urlString = basicUrl + urlString
                    
                    queue.append(urlString)
                    break

        #Checks if current page is clothing
        for regex in info["clothingRegex"]:
            search = regex.search(url)
            if search is not None:
                try:
                    #Gets name
                    name = soup.find("h1", {"class":info["nameIdentifier"]}).text

                    #Get all images
                    imageDiv = soup.find("div", {"class": info["imageIdentifier"]}).text
                    imageSrc = []

                    for img in imageDiv.findAll("img"):
                        imageSrc.append(img['src'])
                    
                    if "breadcrumbsIdentifier" in info.keys():
                        search = soup.find("nav", {"aria-label": info["breadcrumbsIdentifier"]})
                        if search == None:
                            search = soup.find("div", {"class": info["breadcrumbsIdentifier"]})
                    
                        for link in search.findAll("a"):
                            gender = scrapertools.getGender(link.text)
                            if gender != "other":
                                break
                    elif "gender" in info.keys():
                        gender = scrapertools.getGender(info["gender"])
                    else:
                        gender = "other"
                    clothingType = scrapertools.getType(name)
                except Exception:
                    continue
                

if __name__ == "__main__":
    main()