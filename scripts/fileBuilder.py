#Matthew Groholski
#Feburary 4th, 2023

import json
import scrapertools
import re

def main():
    scrapertools.cdFile(__file__)

    #Gets input
    name = input("Store Name: ")
    url = input("Store URL: ")

    #Checks url input
    urlCheck = re.fullmatch("https://www\..+\.(com|co)", url)
    if not urlCheck:
        raise ValueError("Invalid URL address format.")

    webpageRegex = []
    count = int(input("Webpage Regex Count: "))

    for i in range(0, count):
        regex = input("Webpage Regex " + str(i + 1) + ": ")
        webpageRegex.append(regex)

    clothingRegex = []
    count = int(input("Clothing Page Regex Count: "))

    for i in range(0, count):
        regex = input("Clothing Page Regex " + str(i + 1) + ": ")
        clothingRegex.append(regex)
    
    nameIdentifier = input("Name Identifier: ")
    genderIdentifier = input("Gender Identifier: ")
    imageIdentifier = input("Image Div Identifier: ")

    with open("../info/" + name.lower() + ".json", 'w') as file:
        print("Writing file " + scrapertools.pwd() + name + ".json")
        data = {
            "name" : name,
            "url" : url,
            "webpageRegex" : webpageRegex,
            "clothingRegex" : clothingRegex,
            "nameIdentifier" : nameIdentifier,
            "genderIdentifier" : genderIdentifier,
            "imageIdentifier" : imageIdentifier
        }
        json.dump(data, file)


if __name__ == "__main__":
    main()