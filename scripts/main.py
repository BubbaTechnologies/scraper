#Matthew Groholski
#Feburary 5th, 2023

import scrapertools
import requests_html, requests, json, re, asyncio
import time, random, os, sys
from bs4 import BeautifulSoup
import io, datetime

TIMEOUT = 30

async def exitProgram(session:requests_html.AsyncHTMLSession, file: io.TextIOWrapper):
    file.close()
    await session.close()
    exit()

async def backToMain(baseUrl: str, session) -> None:
    response = await session.get(baseUrl, headers = scrapertools.getHeaders(useReferer=True))
    scrapertools.printMessage("Received from " + baseUrl + " status code " + str(response.status_code) + '.')
    time.sleep(random.randint(2,10))

def getApiUrl(baseUrl: str, productUrl: str, apiUrl: str) -> str:
    route = productUrl[len(baseUrl):]
    baseMatch = re.search("{baseUrl}", apiUrl)
    if baseMatch:
        apiUrl = apiUrl[:baseMatch.start()] + baseUrl + apiUrl[baseMatch.end():]
    else:
        scrapertools.printMessage("JSON Error! No {baseUrl} in apiUrlEncoding.")
        exit()

    routeMatch = re.search("{route}", apiUrl)
    if routeMatch:
        apiUrl = apiUrl[:routeMatch.start()] + route + apiUrl[routeMatch.end():]
    else:
        scrapertools.printMessage("JSON Error! No {route} in apiUrlEncoding.")
        exit()
    return apiUrl

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

    baseUrl = info["url"]
    queue = [baseUrl]

    session = requests_html.AsyncHTMLSession()
    indexed = [baseUrl]
    nonAcceptCount = 0
    proxyRequests = 0

    filepath = "output/errors.out"
    if os.path.exists(filepath):
        errorFile = open(filepath, "a")
    else:
        errorFile = open(filepath,"w")

    while not len(queue) == 0:
        try:
            urlIndex = random.randrange(len(queue))
            url = queue.pop(urlIndex)

            #Limit proxy requests
            if proxyRequests > 750:
                await exitProgram(session, errorFile)
            elif scrapertools.PROXY_ACTIVE:
                proxyRequests += 1

            requestHeaders = scrapertools.getHeaders()
            response = await session.get(url, headers = requestHeaders, proxies=scrapertools.getProxies())
            await response.html.arender(wait = 4, timeout=TIMEOUT)
            
            scrapertools.printMessage("Received from " + url + " status code " + str(response.status_code) + ".")

            if not response.status_code == 200:
                errorFile.write(datetime.datetime.now().strftime("%H:%M:%S") + f": Recieved {response.status_code} from {url} using {requestHeaders}.\n" )

                nonAcceptCount += 1
                if nonAcceptCount > 10 and not scrapertools.PROXY_ACTIVE:
                    scrapertools.PROXY_ACTIVE = True
                    nonAcceptCount = 0
                    continue
                elif len(queue) == 0 and not scrapertools.PROXY_ACTIVE:
                    #If baseUrl bounces
                    queue = [baseUrl]
                    scrapertools.PROXY_ACTIVE = True
                    nonAcceptCount = 0
                    continue
                elif nonAcceptCount > 10:
                    await exitProgram(session, errorFile)
                else:   
                    time.sleep(5)
                    if random.randint(0,1) == 1:       
                        await backToMain(baseUrl, session)
                    continue
                
            #Resets nonAcceptCount when accepted
            nonAcceptCount = 0

            #Filters through links
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.find_all('a', href = True):
                for regex in info["webpageRegex"] + info["clothingRegex"]:
                    search = re.search(regex, a["href"])
                    if search:
                        urlString = search.group(0)

                        #Removes extra parameters
                        search = re.search("&.+", urlString)
                        if search:
                            urlString = urlString[:search.start()]
                        
                        if urlString not in indexed:
                            indexed.append(urlString)
                            #Checks for baseUrl
                            baseUrlRegex = baseUrl.replace(".", "\.")
                            search = re.search(baseUrlRegex, urlString)
                            if search == None:
                                urlString = baseUrl + urlString

                            scrapertools.printMessage(f"Appending {urlString} to queue.")
                            queue.append(urlString)
                            break

            #Checks if current page is clothing
            for regex in info["clothingRegex"]:
                search = re.search(regex, url)
                if search is not None:
                        if info["api"]:
                            apiUrl = getApiUrl(baseUrl, url, info["apiUrlEncoding"])

                            #Scrape API Website
                            apiResponse = json.loads(requests.get(apiUrl, headers={"Accept":"application/json"}).text)

                            name = scrapertools.getJsonRoute(info["nameKey"].split("/"), 0, apiResponse)
                            clothingType = scrapertools.getType(name)
                            imageSrc = scrapertools.getJsonRoute(info["imageKey"].split("/"), 0, apiResponse)

                            for i in range(len(imageSrc)):
                                if "//" == imageSrc[i][:2]:
                                    imageSrc[i] = "https://" + imageSrc[i][2:]

                            if "genderKey" in info.keys():
                                gender = scrapertools.getGender(scrapertools.getJsonRoute(info["genderKey"].split("/"), 0, apiResponse))
                                if gender == "other" and "tags" in info.keys():
                                    for tag in scrapertools.getJsonRoute(info["tagsKey"].split("/"),0, apiResponse):
                                        gender = scrapertools.getGender(tag)
                                        if gender != "other":
                                            break
                        else:
                            #Scrape HTML content
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
                            clothingType = scrapertools.getType(name)

                        if "gender" in info.keys():
                            gender = scrapertools.getGender(info["gender"])
                        else: 
                            gender = "other"

                        #Edits imageUrls for better resolution
                        for i in range(len(imageSrc)):
                            imageUrl = imageSrc[i]
                            match = re.search("(\?|&)(w|wid|sw)=[0-9]+&?", imageUrl)
                            if match:
                                match2 = re.search("[0-9]+", match.group(0))
                                imageSrc[i] = imageUrl[:match.start()+match2.start()] + "720" + imageUrl[match.start()+match2.end():]

                        clothing = scrapertools.Clothing(name, imageSrc, url, store.id, clothingType, gender)

                        clothing.createClothing()
                        scrapertools.printMessage("Created " + clothing.toString())
            time.sleep(random.randint(2,10))
            if random.randint(0,1) == 1:           
                await backToMain(baseUrl, session)
        except Exception as e:
            _,_,traceback = sys.exc_info()
            scrapertools.printMessage(f"Exception occured while scraping {url} at line number {traceback.tb_lineno}: {str(e)}")
            continue
        
    await exitProgram(session,errorFile)
                

if __name__ == "__main__":
    asyncio.run(main())