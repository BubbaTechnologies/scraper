#Matthew Groholski
#Feburary 5th, 2023

import scrapertools
import requests_html, requests, json, re, asyncio
import time, random, os, sys
from bs4 import BeautifulSoup


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
    queue = [basicUrl]

    session = requests_html.AsyncHTMLSession()
    indexed = []
    nonAcceptCount = 0

    while not len(queue) == 0:
        time.sleep(random.randint(2,7))
        url = queue.pop(0)
        indexed.append(url)

        response = await session.get(url, headers = scrapertools.getHeaders())
        await response.html.arender(scrolldown=5000)
        
        scrapertools.printMessage("Received from " + url + " status code " + str(response.status_code))

        if not response.status_code == 200:
            nonAcceptCount += 1
            if nonAcceptCount > 10:
                await session.close()
                exit()
            else:
                continue
        else:
            nonAcceptCount = 0
            
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
                    search = re.search(basicUrlRegex, urlString)
                    if search == None:
                        urlString = basicUrl + urlString
                    
                    scrapertools.printMessage(f"Appending {urlString} to queue.")
                    queue.append(urlString)
                    break

        #Checks if current page is clothing
        for regex in info["clothingRegex"]:
            search = re.search(regex, url)
            if search is not None:
                try:
                    #Gets name
                    name = soup.find("h1", {"class":info["nameIdentifier"]}).text
                    #Get all images
                    imageDiv = soup.find("div", {"class": info["imageIdentifier"]})
                    imageSrc = []

                    for img in imageDiv.find_all("img"):
                        if img.has_attr('srcset'):
                            imageSrc.append(img['srcset'].split()[0])
                        else:
                            imageUrl = img['src']
                            if re.match("(https://|/)", imageUrl):
                                imageSrc.append(imageUrl)

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
                    print(clothing.toString())
                    
                    await session.close()
                    exit()

                    clothing.createClothing()
                    scrapertools.printMessage("Created " + clothing.toString())
                except Exception as e:
                    _,_,traceback = sys.exc_info()
                    scrapertools.printMessage(f"Exception occured while scraping {url} at line number {traceback.tb_lineno}: {str(e)}")
                    break
        
        time.sleep(random.randint(0,3))           
        await session.get(url, headers = scrapertools.getHeaders())
        exit()

        
                

if __name__ == "__main__":
    asyncio.run(main())