#Matthew Groholski
#Feburary 5th, 2023

import scrapertools
import requests_html, json, re, asyncio
import time, random, sys
from bs4 import BeautifulSoup

clothingArray = []
websites = []

async def backToMain(basicUrl: str, session):
    response = await session.get(basicUrl, headers = scrapertools.getHeaders())
    scrapertools.printMessage("Received from " + basicUrl + " status code " + str(response.status_code))
    time.sleep(random.randint(0,3))


async def main():
    #Opens file
    filename = input()
    jsonFile = open(filename, "r")
    
    info = json.loads(jsonFile.read())

    store:scrapertools.Store = scrapertools.Store(info["name"], info["url"])
    store.id = -1

    basicUrl = info["url"]
    queue = [basicUrl]

    session = requests_html.AsyncHTMLSession()
    indexed = []
    nonAcceptCount = 0

    while not len(queue) == 0 and not len(websites) > 40:
        time.sleep(random.randint(2,7))
        url = queue.pop(0)
        indexed.append(url)
        websites.append(url)


        requestHeaders = scrapertools.getHeaders()
        response = await session.get(url, headers = requestHeaders)
        await response.html.arender(scrolldown=5000)
        
        scrapertools.printMessage("Received from " + url + " status code " + str(response.status_code))

        if not response.status_code == 200:
            nonAcceptCount += 1
            if nonAcceptCount > 10:
                await session.close()
                return
            else:
                if random.randint(0,1) == 1:           
                    await backToMain(basicUrl, session)
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
                    if regex in info["clothingRegex"]:
                        queue.insert(0,urlString)
                    else:
                        queue.append(urlString)
                    break

        #Checks if current page is clothing
        for regex in info["clothingRegex"]:
            search = re.search(regex, url)
            if search is not None:
                clothingArray.append(urlString)
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

                    scrapertools.printMessage("Created " + clothing.toString())
                except Exception as e:
                    _,_,traceback = sys.exc_info()
                    scrapertools.printMessage(f"Exception occured while scraping {url} at line number {traceback.tb_lineno}: {str(e)}")
                    break
        
        time.sleep(random.randint(0,3))
        if random.randint(0,1) == 1:           
            await backToMain(basicUrl, session)
    await session.close()
    return

        
                

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        _,_,traceback = sys.exc_info()
        scrapertools.printMessage(f"Exception occured at line number {traceback.tb_lineno}: {str(e)}")
    
    if (len(websites) > 40):
        print("Success!")
    else:
        print("Unsuccessful!")
    
    print(f"Scraped {len(websites)} websites:")
    for site in websites:
        print(f"{site}")
    print(f"Scraped {len(clothingArray)} clothing:")
    for site in clothingArray:
        print(f"{site}")